"""
MaintenanceRecord entity model.
Tracks equipment maintenance issues and repair status.
Links to equipment, records problem descriptions, timestamps, and resolution status.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class MaintenanceRecord(Base):
    #Table
    __tablename__ = "maintenancerecord"

    #Attributes
    maintenance_id = Column(Integer, primary_key=True, autoincrement=True)
    equipment_id = Column(Integer, ForeignKey('equipment.equipment_id'))  #FK to equipment
    admin_id = Column(Integer, ForeignKey('adminstaff.admin_id'))  #FK to admin
    issue_description = Column(Text, nullable=False)
    reported_at = Column(TIMESTAMP, server_default=func.now())
    resolved_at = Column(TIMESTAMP, nullable=True)
    status = Column(String(20), nullable=False)  #open, in_progress, resolved

    #Relationships
    #N maintenance records belong to 1 equipment
    equipment = relationship("Equipment", back_populates="maintenance_records")
    #N maintenance records created by 1 admin
    admin = relationship("AdminStaff", back_populates="maintenance_records")
