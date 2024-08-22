from typing import Optional, Type

from sqlalchemy.orm import Session

from app.db.models import Administrator
from app.dependecies import get_password_hash


# Create a new administrator
def create_administrator(db: Session, username: str, password: str) -> Administrator:
    hashed_password = get_password_hash(password)
    new_admin = Administrator(username=username, hashed_password=hashed_password)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin


# Get an administrator by username
def get_administrator_by_username(db: Session, username: str) -> Optional[Type[Administrator]]:
    return db.query(Administrator).filter(Administrator.username == username).first()


# Get all administrators
def get_administrators(db: Session):
    return db.query(Administrator).all()


# Update administrator's active status
def update_administrator_status(db: Session, admin_id: int, is_active: bool):
    admin = db.query(Administrator).filter(Administrator.id == admin_id).first()
    if admin:
        admin.is_active = is_active
        db.commit()
        db.refresh(admin)
    return admin
