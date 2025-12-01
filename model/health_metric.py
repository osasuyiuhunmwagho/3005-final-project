"""
HealthMetric entity model.
Stores historical health data entries (weight, heart rate, body fat) for members.
Each entry is timestamped and never overwritten, maintaining a complete history.
Enables tracking of member progress over time.
"""

from sqlalchemy import Column, Integer, Numeric, ForeignKey, DateTime
from sqlalchemy.sql import func
from core.database import Base

class HealthMetric(Base):
    __tablename__ = "healthmetric"

    metric_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("member.member_id"), nullable=False)
    
    weight = Column(Numeric(5, 2), nullable=True)  # Weight in kg/lbs
    heart_rate = Column(Integer, nullable=True)  # Heart rate in bpm
    body_fat = Column(Numeric(5, 2), nullable=True)  # Body fat percentage
    
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
