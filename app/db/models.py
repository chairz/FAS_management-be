# Database Table Schema
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, Float, Text, ForeignKey, Date, Enum, JSON, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from app.enums import EmploymentStatus, MaritalStatus, Sex, ApplicationStatus

Base = declarative_base()


# Manages system administrators.
class Administrator(Base):
    __tablename__ = 'administrators'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, server_default=text('1'))


# Stores personal information for all individuals.
class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    ic_number = Column(String(9), unique=True)
    date_of_birth = Column(Date)
    sex = Column(Enum(Sex), nullable=False)
    employment_status = Column(Enum(EmploymentStatus), nullable=False)
    marital_status = Column(Enum(MaritalStatus), nullable=False)


# Groups individuals into households.
class Household(Base):
    __tablename__ = 'households'
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(100))

    members = relationship("HouseholdMember", back_populates="household")


# Links individuals to households with their relationship to the applicant.
class HouseholdMember(Base):
    __tablename__ = 'household_members'
    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(Integer, ForeignKey('households.id'))
    person_id = Column(Integer, ForeignKey('persons.id'))
    relation_to_applicant = Column(String(20))

    household = relationship("Household", back_populates="members")
    person = relationship("Person")


# Stores financial schemes and their eligibility criteria.
class Scheme(Base):
    __tablename__ = 'schemes'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    description = Column(String(255))
    marital_status_required = Column(Enum(MaritalStatus), nullable=True)
    employment_status_required = Column(Enum(EmploymentStatus), nullable=True)
    required_relationships = Column(JSON, nullable=True)  # List of required relationships (e.g. ["Spouse", "Child"])
    household_size: Optional[int] = Column(Integer, nullable=True)

    benefits = relationship("Benefit", back_populates="scheme", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="scheme")


# Links individuals who have applied for schemes to their Person and Household records.
class Applicant(Base):
    __tablename__ = 'applicants'
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey('persons.id'))
    household_id = Column(Integer, ForeignKey('households.id'))

    person = relationship("Person")
    household = relationship("Household")
    applications = relationship("Application", back_populates="applicant")


# Tracks specific applications with their submission dates.
class Application(Base):
    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(Integer, ForeignKey('applicants.id'))
    scheme_id = Column(Integer, ForeignKey('schemes.id'))
    application_date = Column(DateTime, default=datetime.utcnow, server_default=text("CURRENT_TIMESTAMP"))
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING.value, server_default=text(f"'{ApplicationStatus.PENDING.value}'"))

    applicant = relationship("Applicant", back_populates="applications")
    scheme = relationship("Scheme", back_populates="applications")


# Describes the benefits associated with each scheme.
class Benefit(Base):
    __tablename__ = 'benefits'
    id = Column(Integer, primary_key=True, index=True)
    scheme_id = Column(Integer, ForeignKey('schemes.id'))
    description = Column(String(255))
    amount = Column(Integer, nullable=True)
    condition = Column(String(255), nullable=True)

    scheme = relationship("Scheme", back_populates="benefits")
