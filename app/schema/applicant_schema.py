from datetime import date

from pydantic import BaseModel
from typing import List, Optional

from app.enums import MaritalStatus, EmploymentStatus, Sex


class HouseholdMemberCreate(BaseModel):
    name: str
    ic_number: str
    date_of_birth: str
    sex: Sex
    employment_status: EmploymentStatus
    marital_status: MaritalStatus
    relation_to_applicant: str


class ApplicantCreate(BaseModel):
    name: str
    ic_number: str
    date_of_birth: str
    sex: Sex
    employment_status: EmploymentStatus
    marital_status: MaritalStatus
    household_id: Optional[int] = None
    address: Optional[str] = None
    household_members: Optional[List[HouseholdMemberCreate]] = None


class ApplicantUpdate(BaseModel):
    name: Optional[str] = None
    ic_number: Optional[str] = None
    date_of_birth: Optional[str] = None
    sex: Optional[Sex] = None
    employment_status: Optional[EmploymentStatus] = None
    marital_status: Optional[MaritalStatus] = None


class HouseholdMemberResponse(BaseModel):
    id: int
    name: str
    ic_number: str
    relation_to_applicant: str

    class Config:
        orm_mode = True


class ApplicantResponse(BaseModel):
    id: int
    name: str
    ic_number: str
    date_of_birth: date
    sex: str
    employment_status: str
    marital_status: str
    household_id: Optional[int]

    class Config:
        orm_mode = True
