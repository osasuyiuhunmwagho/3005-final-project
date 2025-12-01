"""
TrainerAvailability entity model.
Stores time windows when trainers are available for sessions or classes.
Prevents scheduling conflicts by defining available time slots.
"""

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from core.database import Base

class TrainerAvailability(Base):
    __tablename__ = "traineravailability"

    availability_id = Column(Integer, primary_key=True, index=True)

    # Connect availability to a trainer
    trainer_id = Column(Integer, ForeignKey("trainer.trainer_id"), nullable=False)

    # Availability time window
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
