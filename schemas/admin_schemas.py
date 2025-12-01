"""
Admin request/response schemas - data validation and serialization.
Defines Pydantic models for admin operations (room booking, maintenance, class management, billing).
Validates administrative data inputs and formats responses.
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

#============================================
#AdminStaff Schemas
#============================================
class AdminBase(BaseModel):
    """Base schema for AdminStaff"""
    name: str
    email: EmailStr
    role: Optional[str] = None

class AdminCreate(AdminBase):
    """Schema for creating a new admin"""
    pass

class AdminUpdate(BaseModel):
    """Schema for updating admin"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None


class AdminResponse(AdminBase):
    """Schema for admin response"""
    admin_id: int
    
    class Config:
        from_attributes = True  #Allows Pydantic to read from ORM models

#============================================
#Room Schemas
#============================================
class RoomBase(BaseModel):
    """Base schema for Room"""
    room_name: str
    capacity: int
    location: str


class RoomCreate(RoomBase):
    """Schema for creating a new room"""
    admin_id: int


class RoomUpdate(BaseModel):
    """Schema for updating room"""
    room_name: Optional[str] = None
    capacity: Optional[int] = None
    location: Optional[str] = None


class RoomResponse(RoomBase):
    """Schema for room response"""
    room_id: int
    admin_id: int
    
    class Config:
        from_attributes = True

#============================================
#Equipment Schemas
#============================================
class EquipmentBase(BaseModel):
    """Base schema for Equipment"""
    name: str
    status: str  #working, broken, in_repair


class EquipmentCreate(EquipmentBase):
    """Schema for creating new equipment"""
    room_id: int


class EquipmentUpdate(BaseModel):
    """Schema for updating equipment"""
    name: Optional[str] = None
    status: Optional[str] = None
    room_id: Optional[int] = None


class EquipmentResponse(EquipmentBase):
    """Schema for equipment response"""
    equipment_id: int
    room_id: int
    
    class Config:
        from_attributes = True

#============================================
#Maintenance Record Schemas
#============================================

class MaintenanceBase(BaseModel):
    """Base schema for MaintenanceRecord"""
    issue_description: str
    status: str = "open"  #open, in_progress, resolved


class MaintenanceCreate(MaintenanceBase):
    """Schema for creating maintenance record"""
    equipment_id: int
    admin_id: int


class MaintenanceUpdate(BaseModel):
    """Schema for updating maintenance record"""
    status: Optional[str] = None
    resolved_at: Optional[datetime] = None


class MaintenanceResponse(MaintenanceBase):
    """Schema for maintenance response"""
    maintenance_id: int
    equipment_id: int
    admin_id: int
    reported_at: datetime
    resolved_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

#============================================
# Group Class Schemas (Your Feature)
#============================================
class GroupClassCreate(BaseModel):
    "Schema for creating a new group class"
    class_name: str
    trainer_id: int
    room_id: int
    start_time: datetime
    end_time: datetime
    capacity: int

#============================================
# Personal Training Session Schemas (Your Feature)
#============================================
class PTScheduleCreate(BaseModel):
    "Schema for scheduling a personal training session"
    member_id: int
    trainer_id: int
    room_id: int
    start_time: datetime
    end_time: datetime