"""
Member request/response schemas - data validation and serialization.
Defines Pydantic models for member-related API requests and responses.
Validates input data and formats output for member endpoints.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class MemberBase(BaseModel):
    """Base schema for Member"""
    name: str
    email: EmailStr
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    phone: Optional[str] = None

class MemberCreate(MemberBase):
    """Schema for creating a new member"""
    pass

class MemberUpdate(BaseModel):
    """Schema for updating member"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    phone: Optional[str] = None

class MemberResponse(MemberBase):
    """Schema for member response"""
    member_id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Allows Pydantic to read from ORM models

# Health Metric Schemas
class HealthMetricBase(BaseModel):
    """Base schema for HealthMetric"""
    weight: Optional[Decimal] = None
    heart_rate: Optional[int] = None
    body_fat: Optional[Decimal] = None

class HealthMetricCreate(HealthMetricBase):
    """Schema for creating a new health metric"""
    member_id: int

class HealthMetricResponse(HealthMetricBase):
    """Schema for health metric response"""
    metric_id: int
    member_id: int
    recorded_at: datetime
    
    class Config:
        from_attributes = True

# Class Registration Schemas
class ClassRegistrationBase(BaseModel):
    """Base schema for ClassRegistration"""
    member_id: int
    class_id: int

class ClassRegistrationCreate(ClassRegistrationBase):
    """Schema for creating a new class registration"""
    pass

class ClassRegistrationResponse(ClassRegistrationBase):
    """Schema for class registration response"""
    registration_id: int
    registered_at: datetime
    
    class Config:
        from_attributes = True

# Fitness Goal Schemas
class FitnessGoalBase(BaseModel):
    """Base schema for FitnessGoal"""
    goal_type: str
    target_value: Optional[Decimal] = None
    current_value: Optional[Decimal] = None
    target_date: Optional[date] = None
    is_active: bool = True

class FitnessGoalCreate(FitnessGoalBase):
    """Schema for creating a new fitness goal"""
    member_id: int

class FitnessGoalUpdate(BaseModel):
    """Schema for updating a fitness goal"""
    goal_type: Optional[str] = None
    target_value: Optional[Decimal] = None
    current_value: Optional[Decimal] = None
    target_date: Optional[date] = None
    is_active: Optional[bool] = None

class FitnessGoalResponse(FitnessGoalBase):
    """Schema for fitness goal response"""
    goal_id: int
    member_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
