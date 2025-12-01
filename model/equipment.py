"""
Equipment entity model.
Represents gym equipment items assigned to specific rooms.
Tracks equipment status (working/broken/in_repair) for maintenance management.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class Equipment(Base):
    #Table
    __tablename__ = "equipment"

    #Attributes
    equipment_id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey('room.room_id'))  #FK to room
    name = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False)  #working, broken, in_repair

    #Relationships
    #N equipment belong to 1 room
    room = relationship("Room", back_populates="equipment")
    #1 equipment has N maintenance records
    maintenance_records = relationship("MaintenanceRecord", back_populates="equipment", cascade="all, delete-orphan")