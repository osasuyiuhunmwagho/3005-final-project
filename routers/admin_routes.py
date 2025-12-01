"""
Admin API routes - REST endpoints for administrative operations.
Exposes HTTP endpoints for room booking, equipment maintenance, class management, and billing.
Handles admin authentication and administrative functionality.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from core.database import get_db
from schemas.admin_schemas import (
    AdminCreate, AdminUpdate, AdminResponse,
    RoomCreate, RoomUpdate, RoomResponse,
    EquipmentCreate, EquipmentUpdate, EquipmentResponse,
    MaintenanceCreate, MaintenanceUpdate, MaintenanceResponse,
    GroupClassCreate, PTScheduleCreate, 
)
from repositories import admin_repository, room_repository, equipment_repository, maintenance_repository, group_class_repository, session_repository
from model.group_class import GroupClass
from model.personal_training_session import PersonalTrainingSession
from services import admin_service, class_service, booking_service

router = APIRouter(prefix="/admin", tags=["Admin"])
#============================================
#ADMIN CRUD Operations
#============================================
@router.post("/", response_model=AdminResponse, status_code=status.HTTP_201_CREATED)
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    """Create a new admin staff member"""
    #Check if email already exists(unique)
    existing = admin_repository.get_admin_by_email(db, admin.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return admin_repository.create_admin(db, admin.name, admin.email, admin.role)

@router.get("/", response_model=List[AdminResponse])
def get_all_admins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all admins with pagination"""
    return admin_repository.get_all_admins(db, skip, limit)

@router.get("/email/{email}", response_model=AdminResponse)
def get_admin_by_email(email: str, db: Session = Depends(get_db)):
    """Get admin by email address"""
    admin = admin_repository.get_admin_by_email(db, email)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin

@router.get("/by-id/{admin_id}", response_model=AdminResponse)
def get_admin(admin_id: int, db: Session = Depends(get_db)):
    """Get admin by ID"""
    admin = admin_repository.get_admin_by_id(db, admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin

@router.put("/by-id/{admin_id}", response_model=AdminResponse)
def update_admin(admin_id: int, admin_update: AdminUpdate, db: Session = Depends(get_db)):
    """Update admin information"""
    #Check if email is being changed & verify uniqueness
    if admin_update.email:
        existing = admin_repository.get_admin_by_email(db, admin_update.email)
        if existing and existing.admin_id != admin_id:
            raise HTTPException(status_code=400, detail="Email already registered to another admin")
    
    updated = admin_repository.update_admin(
        db, admin_id, 
        admin_update.name, 
        admin_update.email, 
        admin_update.role
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Admin not found")
    return updated

@router.delete("/by-id/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    """Delete an admin"""
    success = admin_repository.delete_admin(db, admin_id)
    if not success:
        raise HTTPException(status_code=404, detail="Admin not found")

#============================================
#ROOM Management
#============================================
@router.post("/rooms", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    """Create a new room"""
    return room_repository.create_room(
        db, room.room_name, room.capacity, room.location, room.admin_id
    )

@router.get("/rooms", response_model=List[RoomResponse])
def get_all_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all rooms"""
    return room_repository.get_all_rooms(db, skip, limit)

@router.get("/rooms/capacity/{min_capacity}", response_model=List[RoomResponse])
def get_rooms_by_capacity(min_capacity: int, db: Session = Depends(get_db)):
    """Get rooms with at least the specified capacity"""
    return room_repository.get_rooms_by_capacity(db, min_capacity)

@router.get("/rooms/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    """Get room by ID"""
    room = room_repository.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.put("/rooms/{room_id}", response_model=RoomResponse)
def update_room(room_id: int, room_update: RoomUpdate, db: Session = Depends(get_db)):
    """Update room information"""
    updated = room_repository.update_room(
        db, room_id, 
        room_update.room_name, 
        room_update.capacity, 
        room_update.location
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Room not found")
    return updated

@router.delete("/rooms/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    """Delete a room"""
    success = room_repository.delete_room(db, room_id)
    if not success:
        raise HTTPException(status_code=404, detail="Room not found")
    
#============================================
#EQUIPMENT Management
#============================================
@router.post("/equipment", response_model=EquipmentResponse, status_code=status.HTTP_201_CREATED)
def create_equipment(equipment: EquipmentCreate, db: Session = Depends(get_db)):
    """Create new equipment"""
    return equipment_repository.create_equipment(
        db, equipment.room_id, equipment.name, equipment.status
    )

@router.get("/equipment", response_model=List[EquipmentResponse])
def get_all_equipment(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all equipment"""
    return equipment_repository.get_all_equipment(db, skip, limit)

@router.get("/equipment/room/{room_id}", response_model=List[EquipmentResponse])
def get_equipment_by_room(room_id: int, db: Session = Depends(get_db)):
    """Get all equipment in a specific room"""
    return equipment_repository.get_equipment_by_room(db, room_id)

@router.get("/equipment/status/{status}", response_model=List[EquipmentResponse])
def get_equipment_by_status(status: str, db: Session = Depends(get_db)):
    """Get equipment by status (working, broken, in_repair)"""
    return equipment_repository.get_equipment_by_status(db, status)

@router.get("/equipment/{equipment_id}", response_model=EquipmentResponse)
def get_equipment(equipment_id: int, db: Session = Depends(get_db)):
    """Get equipment by ID"""
    equipment = equipment_repository.get_equipment_by_id(db, equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment

@router.put("/equipment/{equipment_id}", response_model=EquipmentResponse)
def update_equipment(equipment_id: int, equipment_update: EquipmentUpdate, db: Session = Depends(get_db)):
    """Update equipment information"""
    updated = equipment_repository.update_equipment(
        db, equipment_id, 
        equipment_update.name, 
        equipment_update.status,
        equipment_update.room_id
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return updated

@router.delete("/equipment/{equipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_equipment(equipment_id: int, db: Session = Depends(get_db)):
    """Delete equipment"""
    success = equipment_repository.delete_equipment(db, equipment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Equipment not found")

#============================================
#MAINTENANCE Operations
#============================================
@router.post("/maintenance/report")
def report_equipment_issue(maintenance: MaintenanceCreate, db: Session = Depends(get_db)):
    """Report equipment issue and create maintenance record"""
    result = admin_service.report_equipment_issue(
        db, maintenance.equipment_id, maintenance.admin_id, maintenance.issue_description
    )
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@router.get("/maintenance", response_model=List[MaintenanceResponse])
def get_all_maintenance(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all maintenance records"""
    return maintenance_repository.get_all_maintenance_records(db, skip, limit)

@router.get("/maintenance/equipment/{equipment_id}", response_model=List[MaintenanceResponse])
def get_maintenance_by_equipment(equipment_id: int, db: Session = Depends(get_db)):
    """Get all maintenance records for specific equipment"""
    return maintenance_repository.get_maintenance_by_equipment(db, equipment_id)

@router.get("/maintenance/status/{status}", response_model=List[MaintenanceResponse])
def get_maintenance_by_status(status: str, db: Session = Depends(get_db)):
    """Get maintenance records by status (open, in_progress, resolved)"""
    return maintenance_repository.get_maintenance_by_status(db, status)

@router.get("/maintenance/{maintenance_id}", response_model=MaintenanceResponse)
def get_maintenance_record(maintenance_id: int, db: Session = Depends(get_db)):
    """Get maintenance record by ID"""
    record = maintenance_repository.get_maintenance_record_by_id(db, maintenance_id)
    if not record:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    return record

@router.put("/maintenance/{maintenance_id}/resolve")
def resolve_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    """Mark maintenance issue as resolved"""
    result = admin_service.resolve_equipment_issue(db, maintenance_id)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return result

@router.put("/maintenance/{maintenance_id}", response_model=MaintenanceResponse)
def update_maintenance_status(maintenance_id: int, maintenance_update: MaintenanceUpdate, db: Session = Depends(get_db)):
    """Update maintenance record status"""
    updated = maintenance_repository.update_maintenance_status(
        db, 
        maintenance_id, 
        maintenance_update.status,
        maintenance_update.resolved_at
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    return updated

@router.delete("/maintenance/{maintenance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_maintenance_record(maintenance_id: int, db: Session = Depends(get_db)):
    """Delete a maintenance record"""
    success = maintenance_repository.delete_maintenance_record(db, maintenance_id)
    if not success:
        raise HTTPException(status_code=404, detail="Maintenance record not found")

#============================================
#GROUP CLASS Management
#============================================
@router.post("/classes", status_code=201)
def create_group_class(data: GroupClassCreate, db: Session = Depends(get_db)):
    """
    Creates a new group fitness class.
    Ensures:
      - room is not double-booked
      - trainer is not double-booked
    """

    # Room conflict check
    if group_class_repository.room_conflict(db, data.room_id, data.start_time, data.end_time):
        raise HTTPException(status_code=400, detail="Room is already booked for this time.")

    # Trainer conflict check
    if group_class_repository.trainer_conflict(db, data.trainer_id, data.start_time, data.end_time):
        raise HTTPException(status_code=400, detail="Trainer is already teaching another class.")

    # Create & save class
    new_class = GroupClass(**data.dict())
    return group_class_repository.create_class(db, new_class)

# ============================================================
# PERSONAL TRAINING SESSION SCHEDULING
# ============================================================
@router.post("/pt-session", status_code=201)
def schedule_pt_session(data: PTScheduleCreate, db: Session = Depends(get_db)):
    """
    Schedules a personal training session.
    """

    # Trainer must be available
    if not session_repository.trainer_available(db, data.trainer_id, data.start_time, data.end_time):
        raise HTTPException(status_code=400, detail="Trainer is not available during this time.")

    # Trainer must not have another PT session
    if session_repository.trainer_session_conflict(db, data.trainer_id, data.start_time, data.end_time):
        raise HTTPException(status_code=400, detail="Trainer already has another session at this time.")

    # Room must be free
    if session_repository.room_conflict(db, data.room_id, data.start_time, data.end_time):
        raise HTTPException(status_code=400, detail="Room is already booked.")

    # Create session
    session = PersonalTrainingSession(**data.dict(), status="scheduled")
    return session_repository.create_session(db, session)

#============================================
#ROOM Availability Check
#============================================
@router.get("/rooms/{room_id}/availability")
def check_room_availability(
    room_id: int,
    start_time: datetime,
    end_time: datetime,
    db: Session = Depends(get_db)
):
    """Check if a room is available for a given time slot"""
    result = booking_service.check_room_availability(db, room_id, start_time, end_time)
    return result
