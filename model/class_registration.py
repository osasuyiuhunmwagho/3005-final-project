"""
ClassRegistration entity model.
Junction table linking members to group classes (many-to-many relationship).
Tracks when members register for classes to manage enrollment.
"""

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class ClassRegistration(Base):
    __tablename__ = "classregistration"

    registration_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("member.member_id"), nullable=False)
    class_id = Column(Integer, ForeignKey("groupclass.class_id"), nullable=False)
    registered_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    member = relationship("Member", back_populates="class_registrations")
    group_class = relationship("GroupClass", back_populates="registrations")
