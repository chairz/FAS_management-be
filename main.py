from app.config.logging_config import LOGGING_CONFIG
from app.db.database import engine
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from starlette.responses import JSONResponse

from app.db import models
from app.router import auth, schemes, applicants, applications
import logging.config

# Initialize FastAPI app
app = FastAPI()
# Include routers
app.include_router(auth.router)
app.include_router(schemes.router)
app.include_router(applicants.router)
app.include_router(applications.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    detailed_errors = []
    for error in errors:
        loc = error.get("loc", [])
        msg = error.get("msg", "")
        error_type = error.get("type", "")

        missing_field = None
        if error_type == "missing":
            if loc[0] == "body" and len(loc) > 1:
                missing_field = loc[1]

        detailed_error = {
            "loc": loc,
            "msg": msg,
            "type": error_type,
            "missing_field": missing_field
        }
        detailed_errors.append(detailed_error)

    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({
            "detail": detailed_errors
        }),
    )


# Initialize logging
logging.config.dictConfig(LOGGING_CONFIG)

# Create the database tables
models.Base.metadata.create_all(bind=engine)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Financial Assistance Scheme Management System",
        version="1.0.0",
        description="API Documentation",
        routes=app.routes
    )

    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT token here",
        }
    }
    # Apply security only to specific methods on specific paths
    paths_to_protect = [
        ("POST", "/api/scheme"),
        ("GET", "/api/schemes/eligible"),
        ("POST", "/api/applicants"),
        ("GET", "/api/applicants/{applicant_id}"),
        ("PUT", "/api/applicants/{applicant_id}"),
        ("DELETE", "/api/applicants/{applicant_id}"),
        ("GET", "/api/applicants"),
        ("POST", "/api/applications"),
        ("GET", "/api/applications"),
        ("GET", "/api/applications/search"),
        ("GET", "/api/applications/{application_id}"),
        ("PUT", "/api/applications/{application_id}"),
        ("DELETE", "/api/applications/{application_id}"),
    ]

    for method, path in paths_to_protect:
        if path in openapi_schema["paths"]:
            if method.lower() in openapi_schema["paths"][path]:
                openapi_schema["paths"][path][method.lower()]["security"] = [{"BearerAuth": []}]

    # Organize endpoints by tags
    openapi_schema["tags"] = [
        {"name": "Admin", "description": "Operations related to admin management. "},
        {"name": "Schemes", "description": "Operations related to financial assistance schemes."},
        {"name": "Applicants", "description": "Operations related to applicants."},
        {"name": "Applications", "description": "Operations related to applications for financial assistance."},
        ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Set the custom OpenAPI schema
app.openapi = custom_openapi

# Run the app
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
