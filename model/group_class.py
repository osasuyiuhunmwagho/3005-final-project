"""
GroupClass entity model.
Represents fitness classes with name, instructor (trainer), room assignment, and schedule.
Tracks class capacity for enrollment management.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from core.database import Base

class GroupClass(Base):
    __tablename__ = "GroupClass"

    class_id = Column(Integer, primary_key=True, index=True)

    class_name = Column(String(100), nullable=False)

    trainer_id = Column(Integer, ForeignKey("Trainer.trainer_id"), nullable=False)
    room_id = Column(Integer, ForeignKey("Room.room_id"), nullable=False)

    # Time range for class
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    capacity = Column(Integer, nullable=False)


