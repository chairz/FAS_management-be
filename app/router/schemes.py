from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.applicant_table import get_applicant_by_id
from app.crud.scheme_table import get_all_schemes, get_eligible_schemes_for_applicant, create_scheme
from app.db.database import get_db
from app.dependecies import get_current_user
from app.schema.auth_schema import User
from app.schema.scheme_schema import SchemeResponse, SchemeCreate

router = APIRouter()


@router.post(
    "/api/scheme",
    response_model=SchemeResponse,
    description="This endpoint allows an authenticated user to create a new financial assistance scheme.",
    tags=["Schemes"]
)
async def create_new_scheme(current_user: Annotated[User, Depends(get_current_user)], scheme: SchemeCreate,
                            db: Session = Depends(get_db)):
    return create_scheme(db, scheme)


@router.get(
    "/api/schemes",
    response_model=list[SchemeResponse],
    summary="Get All Schemes",
    description="This endpoint retrieves all available financial assistance schemes, including their details and eligibility criteria.",
    tags=["Schemes"]
)
async def read_schemes(db: Session = Depends(get_db)):
    schemes = get_all_schemes(db)
    return schemes


@router.get(
    "/api/schemes/eligible",
    response_model=list[SchemeResponse],
    description="""
    This endpoint retrieves a list of financial assistance schemes that a specific applicant is eligible to apply for.
    The eligibility is determined based on the applicant's data using marital status, employment status, and household members.
    """,
    tags=["Schemes"]
)
async def read_eligible_schemes(current_user: Annotated[User, Depends(get_current_user)], applicant_id: int,
                                db: Session = Depends(get_db)):
    applicant = get_applicant_by_id(db, applicant_id)
    if applicant is None:
        raise HTTPException(status_code=404, detail="Applicant not found")

    schemes = get_eligible_schemes_for_applicant(db, applicant)
    return schemes
