from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from typing import List, Annotated

from app.crud.applicant_table import create_applicant, get_applicant_by_id, update_applicant, delete_applicant, \
    list_applicants
from app.db.database import get_db
from app.dependecies import get_current_user
from app.schema.applicant_schema import ApplicantResponse, ApplicantCreate, ApplicantUpdate
from app.schema.auth_schema import User

router = APIRouter()


@router.post(
    "/api/applicants",
    response_model=ApplicantResponse,
    description="Create a new applicant.",
    tags=["Applicants"]
)
async def create_new_applicant(current_user: Annotated[User, Depends(get_current_user)], applicant: ApplicantCreate, db: Session = Depends(get_db)):
    new_applicant = create_applicant(db, applicant)
    response_data = {
        "id": new_applicant.id,
        "name": new_applicant.person.name,
        "ic_number": new_applicant.person.ic_number,
        "date_of_birth": new_applicant.person.date_of_birth,
        "sex": new_applicant.person.sex,
        "employment_status": new_applicant.person.employment_status,
        "marital_status": new_applicant.person.marital_status,
        "household_id": new_applicant.household_id
    }
    return response_data


@router.get(
    "/api/applicants/{applicant_id}",
    response_model=ApplicantResponse,
    description="Retrieve an applicant by their ID.",
    tags=["Applicants"]
)
async def get_single_applicant(current_user: Annotated[User, Depends(get_current_user)], applicant_id: int, db: Session = Depends(get_db)):
    applicant = get_applicant_by_id(db, applicant_id)
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")
    response_data = {
        "id": applicant.id,
        "name": applicant.person.name,
        "ic_number": applicant.person.ic_number,
        "date_of_birth": applicant.person.date_of_birth,
        "sex": applicant.person.sex,
        "employment_status": applicant.person.employment_status,
        "marital_status": applicant.person.marital_status,
        "household_id": applicant.household_id
    }
    return response_data


@router.put(
    "/api/applicants/{applicant_id}",
    response_model=ApplicantResponse,
    description="Update an applicant's details.",
    tags=["Applicants"]
)
async def update_existing_applicant(current_user: Annotated[User, Depends(get_current_user)], applicant_id: int, applicant_update: ApplicantUpdate,
                                    db: Session = Depends(get_db)):
    updated_applicant = update_applicant(db, applicant_id, applicant_update)
    if not updated_applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")
    response_data = {
        "id": updated_applicant.id,
        "name": updated_applicant.person.name,
        "ic_number": updated_applicant.person.ic_number,
        "date_of_birth": updated_applicant.person.date_of_birth,
        "sex": updated_applicant.person.sex,
        "employment_status": updated_applicant.person.employment_status,
        "marital_status": updated_applicant.person.marital_status,
        "household_id": updated_applicant.household_id
    }
    return response_data


@router.delete(
    "/api/applicants/{applicant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete an applicant by their ID.",
    tags=["Applicants"]
)
async def delete_existing_applicant(current_user: Annotated[User, Depends(get_current_user)], applicant_id: int, db: Session = Depends(get_db)):
    applicant = delete_applicant(db, applicant_id)
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")
    return


@router.get(
    "/api/applicants",
    response_model=List[ApplicantResponse],
    description="Retrieve a list of all applicants.",
    tags=["Applicants"]
)
async def list_all_applicants(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    applicants = list_applicants(db)

    response_data = []
    for applicant in applicants:
        response_data.append({
            "id": applicant.id,
            "name": applicant.person.name,
            "ic_number": applicant.person.ic_number,
            "date_of_birth": applicant.person.date_of_birth,
            "sex": applicant.person.sex,
            "employment_status": applicant.person.employment_status,
            "marital_status": applicant.person.marital_status,
            "household_id": applicant.household_id
        })

    return response_data
