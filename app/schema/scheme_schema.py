from typing import Optional, List

from pydantic import BaseModel, Field


class BenefitCreate(BaseModel):
    description: str = Field(..., description="Description of the benefit (e.g., 'Monthly food vouchers').")
    amount: Optional[int] = Field(None, description="Monetary value of the benefit, if applicable.")
    condition: Optional[str] = Field(None, description="Condition that must be met for this benefit.")


class SchemeCreate(BaseModel):
    name: str = Field(..., description="The name of the scheme (e.g., 'Family Support Scheme').")
    description: str = Field(..., description="A brief description of the scheme.")
    marital_status_required: Optional[str] = Field(None,
                                                   description="Marital status required to be eligible for the scheme.")
    employment_status_required: Optional[str] = Field(None,
                                                      description="Employment status required to be eligible for the scheme.")
    required_relationships: Optional[List[str]] = Field(None,
                                                        description="List of specific relationships required within the household.")
    household_size: Optional[int] = Field(None, description="Minimum household size required to be eligible.")
    benefits: List[BenefitCreate] = Field(..., description="List of benefits associated with the scheme.")


class BenefitResponse(BaseModel):
    id: int
    description: str
    amount: Optional[int]
    condition: Optional[str]

    class Config:
        orm_mode = True


class SchemeResponse(BaseModel):
    id: int
    name: str
    description: str
    marital_status_required: Optional[str] = None
    employment_status_required: Optional[str] = None
    required_relationships: Optional[List[str]] = None
    household_size: Optional[int] = None
    benefits: List[BenefitResponse]

    class Config:
        orm_mode = True
