"""
Trainer request/response schemas - data validation and serialization.
Defines Pydantic models for trainer-related API requests and responses.
Validates availability scheduling, schedule queries, and member lookup requests.
"""
from pydantic import BaseModel, EmailStr
from typing import Optional

class TrainerCreate(BaseModel):
    name: str
    email: EmailStr
    specialization: Optional[str] = None
    phone: Optional[str] = None

class TrainerResponse(BaseModel):
    trainer_id: int
    name: str
    email: EmailStr
    specialization: Optional[str]
    phone: Optional[str]

    class Config:
        orm_mode = True

