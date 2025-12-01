"""
FitnessGoal entity model.
Represents member fitness objectives (e.g., weight loss targets).
Links goals to members and tracks whether goals are currently active.
Stores target values and creation timestamps for progress tracking.
"""

from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Date, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class FitnessGoal(Base):
    __tablename__ = "fitnessgoal"

    goal_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("member.member_id"), nullable=False)
    
    goal_type = Column(String(50), nullable=False)  # e.g., "weight_loss", "muscle_gain", "endurance"
    target_value = Column(Numeric(10, 2), nullable=True)
    current_value = Column(Numeric(10, 2), nullable=True)
    target_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    member = relationship("Member", back_populates="fitness_goals")
