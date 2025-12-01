"""
Trainer entity model.
Represents fitness trainers with contact information and specialization.
Used for personal training sessions and group class instruction.
"""

from sqlalchemy import Column, Integer, String
from core.database import Base

class Trainer(Base):
    __tablename__ = "Trainer"

    trainer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    specialization = Column(String(100))
    phone = Column(String(20))

