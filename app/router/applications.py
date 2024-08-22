from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.application_table import create_application, get_application_by_id, update_application, delete_application, list_applications
from app.db.database import get_db
from app.db.models import Scheme, Applicant, HouseholdMember, Application
from app.dependecies import get_current_user
from app.enums import ApplicationStatus
from app.schema.auth_schema import User
from app.schema.application_schema import ApplicationResponse, ApplicationCreate, ApplicationUpdate

router = APIRouter()


@router.post(
    "/api/applications",
    response_model=ApplicationResponse,
    description="Create a new application for a financial assistance scheme.",
    tags=["Applications"]
)
async def create_new_application(current_user: Annotated[User, Depends(get_current_user)], application: ApplicationCreate,
                                 db: Session = Depends(get_db)):
    # Check if the applicant exists
    applicant = db.query(Applicant).filter(Applicant.id == application.applicant_id).first()
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")

    # Check if the scheme exists
    scheme = db.query(Scheme).filter(Scheme.id == application.scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")

    # Check for existing application with the same scheme and applicant
    existing_application = db.query(Application).filter(
        Application.applicant_id == application.applicant_id,
        Application.scheme_id == application.scheme_id,
        Application.status.in_([ApplicationStatus.PENDING.value])  # Only check for 'Pending' status
    ).first()

    if existing_application:
        raise HTTPException(status_code=400,
                            detail="An application for this scheme by the same applicant already exists and is still pending.")

    # Check eligibility based on the scheme's criteria
    if scheme.marital_status_required and scheme.marital_status_required != applicant.person.marital_status:
        raise HTTPException(status_code=400,
                            detail="Applicant does not meet the marital status requirement for this scheme")

    if scheme.employment_status_required and scheme.employment_status_required != applicant.person.employment_status:
        raise HTTPException(status_code=400,
                            detail="Applicant does not meet the employment status requirement for this scheme")

    if scheme.household_size and scheme.household_size > len(applicant.household.members) + 1:
        raise HTTPException(status_code=400,
                            detail="Applicant's household size does not meet the requirement for this scheme")

    if scheme.required_relationships:
        household_members = db.query(HouseholdMember).filter(
            HouseholdMember.household_id == applicant.household_id).all()
        relationships = [member.relation_to_applicant for member in household_members]

        for required_relationship in scheme.required_relationships:
            if required_relationship not in relationships:
                raise HTTPException(status_code=400,
                                    detail=f"Applicant does not have the required relationship: {required_relationship}")

    return create_application(db, application)


@router.get(
    "/api/applications/search",
    response_model=List[ApplicationResponse],
    description="Search for applications by applicant ID.",
    tags=["Applications"]
)
async def search_applications_by_applicant_id(
        current_user: Annotated[User, Depends(get_current_user)],
        applicant_id: int,
        db: Session = Depends(get_db)
):
    applications = db.query(Application).filter(Application.applicant_id == applicant_id).all()
    if not applications:
        raise HTTPException(status_code=404, detail="No applications found for this applicant.")

    return applications


@router.get(
    "/api/applications/{application_id}",
    response_model=ApplicationResponse,
    description="Retrieve an application by its ID.",
    tags=["Applications"]
)
async def read_application(application_id: int, current_user: Annotated[User, Depends(get_current_user)],
                           db: Session = Depends(get_db)):
    application = get_application_by_id(db, application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.put(
    "/api/applications/{application_id}",
    response_model=ApplicationResponse,
    description="Update an existing application.",
    tags=["Applications"]
)
async def update_existing_application(application_id: int, application_update: ApplicationUpdate,
                                      current_user: Annotated[User, Depends(get_current_user)],
                                      db: Session = Depends(get_db)):
    updated_application = update_application(db, application_id, application_update)
    if updated_application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return updated_application


@router.delete(
    "/api/applications/{application_id}",
    status_code=204,
    description="Delete an application by its ID.",
    tags=["Applications"]
)
async def delete_existing_application(application_id: int, current_user: Annotated[User, Depends(get_current_user)],
                                      db: Session = Depends(get_db)):
    application = delete_application(db, application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return


@router.get(
    "/api/applications",
    response_model=List[ApplicationResponse],
    description="Retrieve a list of all applications.",
    tags=["Applications"]
)
async def list_all_applications(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    return list_applications(db)
