"""
Equipment repository - data access layer for Equipment entities.
Handles equipment data operations and status management.
Queries equipment by room, status, or equipment ID.
"""
from sqlalchemy.orm import Session
from model.equipment import Equipment
from typing import Optional, List

def create_equipment(db: Session, room_id: int, name: str, status: str = "working") -> Equipment:
    """
    Create a new equipment instance for database

    Parameters :
        db      : Database session
        room_id : Room ID where equipment is located
        name    : Equipment name
        status  : Equipment status (default: "working")
    Returns :
        equipment : Created Equipment object
    """
    equipment = Equipment(
        room_id = room_id,
        name = name,
        status = status
    )
    db.add(equipment)       #add to database
    db.commit()             #save changes to database
    db.refresh(equipment)   #re-load database with updates
    return equipment

def get_equipment_by_id(db: Session, equipment_id: int) -> Optional[Equipment]:
    """
    Get equipment by ID
    
    Parameters :
        db           : Database session
        equipment_id : Equipment ID 
    Returns :
        equipment    : Equipment object with matching id or none if nothing found
    """
    #Filter for equipment where the equipment_ids match (first returns the first match or none)
    equipment = db.query(Equipment).filter(Equipment.equipment_id == equipment_id).first()
    return equipment

def get_equipment_by_room(db: Session, room_id: int) -> List[Equipment]:
    """
    Get all equipment in a specific room

    Parameters :
        db      : Database session
        room_id : Room ID
    Returns :
        equipment : List of Equipment objects in that room
    """
    #Filter through ALL equipment in a specific room
    equipment = db.query(Equipment).filter(Equipment.room_id == room_id).all()
    return equipment

def get_equipment_by_status(db: Session, status: str) -> List[Equipment]:
    """
    Get equipment by status (working, broken, in_repair)

    Parameters :
        db     : Database session
        status : Equipment status to filter by
    Returns :
        equipment : List of Equipment objects with that status
    """
    #Filter through ALL equipment with a specific status
    equipment = db.query(Equipment).filter(Equipment.status == status).all()
    return equipment

def get_all_equipment(db: Session, skip: int = 0, limit: int = 100) -> List[Equipment]:
    """
    Get all equipment with pagination

    Parameters :
        db        : Database session
        skip      : Num of records to skip
        limit     : Maximum records to return
    Returns :
        equipment : list of Equipment objects
    """
    #Get every equipment object
    equipment = db.query(Equipment).offset(skip).limit(limit).all()
    return equipment

def update_equipment(db: Session, equipment_id: int, name: Optional[str] = None, status: Optional[str] = None, room_id: Optional[int] = None) -> Optional[Equipment]:
    """
    Update equipment information

    Parameters :
        db           : Database session
        equipment_id : Equipment ID (Equipment we want to update)
        name         : New name (optional)
        status       : New status (optional)
        room_id      : New room ID (optional)
    Returns :
        equipment    : Updated Equipment object or none if not found
    """
    #get equipment by id and if not exists return none
    equipment = get_equipment_by_id(db, equipment_id)
    if not equipment:
        return None
    
    #update features if not none
    if name is not None:
        equipment.name = name
    if status is not None:
        equipment.status = status
    if room_id is not None:
        equipment.room_id = room_id
    
    db.commit()             #save changes to database
    db.refresh(equipment)   #re-load database with updates
    return equipment

def delete_equipment(db: Session, equipment_id: int) -> bool:
    """
    Delete equipment from database

    Parameters :
        db           : Database session
        equipment_id : Equipment ID (Equipment to delete)
    Returns :
        True         : If deletion successful else, False if not found
    """
    #get equipment by id and if not exists return False
    equipment = get_equipment_by_id(db, equipment_id)
    if not equipment:
        return False
    
    db.delete(equipment)    #delete equipment from database
    db.commit()             #save changes to database
    return True


