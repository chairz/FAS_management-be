from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.enums import ApplicationStatus


class ApplicationCreate(BaseModel):
    applicant_id: int
    scheme_id: int


class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = Field(None, description="Update the status of the application.")


class ApplicationResponse(BaseModel):
    id: int
    applicant_id: int
    scheme_id: int
    status: ApplicationStatus
    application_date: datetime

    class Config:
        orm_mode = True
