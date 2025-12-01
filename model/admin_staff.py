"""
AdminStaff entity model.
Represents administrative personnel with system management privileges.
Used for room booking, equipment maintenance, class management, and billing operations.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base

class AdminStaff(Base):
    #Table
    __tablename__ = "adminstaff"
    #Attributes
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(String(50))

    #Relationships 
    #1 admind creates N maintenance records
    maintenance_records = relationship("MaintenanceRecord", back_populates="admin", cascade="all, delete-orphan") 
    #1 admin manages N rooms
    rooms = relationship("Room", back_populates="admin", cascade="all, delete-orphan")
    #1 admin schedules N group classes
    group_classes = relationship("GroupClass", back_populates="admin", cascade="all, delete-orphan")