"""
Member entity model.
Represents a gym member with personal information (name, email, DOB, gender, phone).
Tracks member registration timestamp and serves as the central user entity.
"""

from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class Member(Base):
    __tablename__ = "member"

    member_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(20), nullable=True)
    phone = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    class_registrations = relationship("ClassRegistration", back_populates="member")
    fitness_goals = relationship("FitnessGoal", back_populates="member")
