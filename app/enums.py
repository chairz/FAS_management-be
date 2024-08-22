import enum


class MaritalStatus(enum.Enum):
    SINGLE = "Single"
    MARRIED = "Married"
    WIDOWED = "Widowed"
    DIVORCED = "Divorced"


class EmploymentStatus(enum.Enum):
    EMPLOYED = "Employed"
    UNEMPLOYED = "Unemployed"


class ApplicationStatus(enum.Enum):
    APPROVED = "APPROVED"
    PENDING = "PENDING"
    REJECTED = "REJECTED"


class Sex(enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
