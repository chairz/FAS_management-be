from sqlalchemy.orm import Session
from app.db.models import Applicant, Person, HouseholdMember, Household
from app.schema.applicant_schema import ApplicantCreate, ApplicantUpdate
from typing import List, Optional


def create_applicant(db: Session, applicant: ApplicantCreate) -> Applicant:
    # Create the Person record
    person = db.query(Person).filter(Person.ic_number == applicant.ic_number).first()
    if not person:
        person = Person(
            name=applicant.name,
            ic_number=applicant.ic_number,
            date_of_birth=applicant.date_of_birth,
            sex=applicant.sex,
            employment_status=applicant.employment_status,
            marital_status=applicant.marital_status
        )
        db.add(person)
        db.commit()
        db.refresh(person)

    # Create a new Household record for each applicant
    household = Household(address=applicant.address if applicant.address else "No Address Provided")
    db.add(household)
    db.commit()
    db.refresh(household)

    # Create the Applicant record linked to the newly created Household
    new_applicant = Applicant(
        person_id=person.id,
        household_id=household.id
    )
    db.add(new_applicant)
    db.commit()
    db.refresh(new_applicant)

    # Handle household members if provided
    if applicant.household_members:
        for member in applicant.household_members:
            member_person = db.query(Person).filter(Person.ic_number == member.ic_number).first()
            if not member_person:
                member_person = Person(
                    name=member.name,
                    ic_number=member.ic_number,
                    date_of_birth=member.date_of_birth,
                    sex=member.sex,
                    employment_status=member.employment_status,
                    marital_status=member.marital_status,
                )
                db.add(member_person)
                db.commit()
                db.refresh(member_person)

            new_member = HouseholdMember(
                household_id=household.id,
                person_id=member_person.id,
                relation_to_applicant=member.relation_to_applicant
            )
            db.add(new_member)

        db.commit()

    return new_applicant


def get_applicant_by_id(db: Session, applicant_id: int) -> Optional[Applicant]:
    return db.query(Applicant).filter(Applicant.id == applicant_id).first()


def update_applicant(db: Session, applicant_id: int, applicant_update: ApplicantUpdate) -> Optional[Applicant]:
    applicant = db.query(Applicant).filter(Applicant.id == applicant_id).first()
    if not applicant:
        return None

    person = applicant.person
    for key, value in applicant_update.dict(exclude_unset=True).items():
        if hasattr(person, key):
            setattr(person, key, value)

    db.commit()
    db.refresh(applicant)
    return applicant


def delete_applicant(db: Session, applicant_id: int) -> Optional[Applicant]:
    applicant = db.query(Applicant).filter(Applicant.id == applicant_id).first()
    if not applicant:
        return None

    db.delete(applicant)
    db.commit()
    return applicant


def list_applicants(db: Session) -> List[Applicant]:
    return db.query(Applicant).all()
