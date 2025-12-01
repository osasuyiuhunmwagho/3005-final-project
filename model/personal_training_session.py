"""
PersonalTrainingSession entity model.
Represents one-on-one training sessions between a member and trainer.
Tracks session scheduling, room assignment, time slots, and status (scheduled/cancelled/completed).
"""

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from core.database import Base

class PersonalTrainingSession(Base):
    __tablename__ = "personaltrainingsession"

    session_id = Column(Integer, primary_key=True, index=True)

    member_id = Column(Integer, ForeignKey("member.member_id"), nullable=False)
    trainer_id = Column(Integer, ForeignKey("trainer.trainer_id"), nullable=False)
    room_id = Column(Integer, ForeignKey("room.room_id"), nullable=False)

    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    # scheduled / cancelled / completed
    status = Column(String(20), nullable=False)

    # Relationships
    member = relationship("Member", back_populates="personal_training_sessions")
    trainer = relationship("Trainer", back_populates="personal_training_sessions")
    room = relationship("Room", back_populates="personal_training_sessions")


