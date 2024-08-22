import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.administrator_table import get_administrator_by_username, create_administrator
from app.db.database import get_db
from app.dependecies import authenticate_user, create_access_token, get_current_user
from app.schema.auth_schema import Token, User, LoginRequest, RegisterRequest

router = APIRouter()
logger = logging.getLogger("myapp")


@router.post("/auth/register", description="""
    This endpoint registers an admin to log in and receive an access token.
    """, tags=["Admin"])
async def register_admin(register_req: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = get_administrator_by_username(db, register_req.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    new_admin = create_administrator(db, register_req.username, register_req.password)
    return {"username": new_admin.username, "is_active": new_admin.is_active}


@router.post("/auth/login", response_model=Token, description="""
    This endpoint allows admin to log in and receive an access token.
    The token returned can be used for authentication in subsequent requests by including it in the `Authorization` header as `Bearer <token>`.
    """, tags=["Admin"])
async def login_admin(form_data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

