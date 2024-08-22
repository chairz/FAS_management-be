from typing import Optional, List, Type

from sqlalchemy.orm import Session

from app.db.models import Application
from app.schema.application_schema import ApplicationCreate, ApplicationUpdate


def create_application(db: Session, application_data: ApplicationCreate) -> Application:
    new_application = Application(
        applicant_id=application_data.applicant_id,
        scheme_id=application_data.scheme_id,
    )
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return new_application


def get_application_by_id(db: Session, application_id: int) -> Optional[Application]:
    return db.query(Application).filter(Application.id == application_id).first()


def update_application(db: Session, application_id: int, application_update: ApplicationUpdate) -> Optional[Application]:
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        return None

    for key, value in application_update.dict(exclude_unset=True).items():
        setattr(application, key, value)

    db.commit()
    db.refresh(application)
    return application


def delete_application(db: Session, application_id: int) -> Optional[Application]:
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        return None

    db.delete(application)
    db.commit()
    return application


def list_applications(db: Session) -> list[Type[Application]]:
    return db.query(Application).all()
