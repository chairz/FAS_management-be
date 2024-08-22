from sqlalchemy.orm import Session

from app.db.models import Scheme, HouseholdMember, Benefit
from app.schema.scheme_schema import SchemeCreate


def create_scheme(db: Session, scheme_data: SchemeCreate) -> Scheme:
    # Create the scheme
    new_scheme = Scheme(
        name=scheme_data.name,
        description=scheme_data.description,
        marital_status_required=scheme_data.marital_status_required,
        employment_status_required=scheme_data.employment_status_required,
        required_relationships=scheme_data.required_relationships,
        household_size=scheme_data.household_size
    )
    db.add(new_scheme)
    db.commit()
    db.refresh(new_scheme)

    # Create the associated benefits
    for benefit in scheme_data.benefits:
        new_benefit = Benefit(
            scheme_id=new_scheme.id,
            description=benefit.description,
            amount=benefit.amount,
            condition=benefit.condition
        )
        db.add(new_benefit)

    db.commit()

    return new_scheme


def get_all_schemes(db: Session) -> list[Scheme]:
    return db.query(Scheme).all()


def get_eligible_schemes_for_applicant(db: Session, applicant) -> list[Scheme]:
    schemes = db.query(Scheme).all()
    eligible_schemes = []

    for scheme in schemes:
        if (
            (scheme.marital_status_required is None or scheme.marital_status_required == applicant.person.marital_status) and
            (scheme.employment_status_required is None or scheme.employment_status_required == applicant.person.employment_status) and
            (scheme.household_size is None or scheme.household_size <= len(applicant.household.members))
        ):
            if not scheme.required_relationships:
                eligible_schemes.append(scheme)
                continue

            household_members = db.query(HouseholdMember).filter(HouseholdMember.household_id == applicant.household_id).all()
            relationships = [member.relation_to_applicant for member in household_members]

            if all(req_rel in relationships for req_rel in scheme.required_relationships):
                eligible_schemes.append(scheme)

    return eligible_schemes
