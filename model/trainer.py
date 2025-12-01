"""
Trainer entity model.
Represents fitness trainers with contact information and specialization.
Used for personal training sessions and group class instruction.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base

class Trainer(Base):
    __tablename__ = "trainer"

    trainer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    specialization = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)

    # Relationships
    availabilities = relationship("TrainerAvailability", back_populates="trainer", cascade="all, delete-orphan")
    group_classes = relationship("GroupClass", back_populates="trainer", cascade="all, delete-orphan")
    personal_training_sessions = relationship("PersonalTrainingSession", back_populates="trainer", cascade="all, delete-orphan")

