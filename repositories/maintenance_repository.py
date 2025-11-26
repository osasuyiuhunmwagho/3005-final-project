"""
MaintenanceRecord repository - data access layer for maintenance records.
Handles equipment maintenance issue tracking.
Manages maintenance record creation, status updates, and queries.
"""
from sqlalchemy.orm import Session
from model.maintenance_record import MaintenanceRecord
from typing import Optional, List
from datetime import datetime

def create_maintenance_record(db: Session, equipment_id: int, admin_id: int, issue_description: str, status: str = "open") -> MaintenanceRecord:
    """
    Create a new maintenance record for equipment

    Parameters :
        db                : Database session
        equipment_id      : Equipment ID that needs maintenance
        admin_id          : Admin ID who created the record
        issue_description : Description of the maintenance issue
        status            : Status of maintenance (default: "open")
    Returns :
        record            : Created MaintenanceRecord object
    """
    record = MaintenanceRecord(
        equipment_id = equipment_id,
        admin_id = admin_id,
        issue_description = issue_description,
        status = status
    )
    db.add(record)       #add to database
    db.commit()          #save changes to database
    db.refresh(record)   #re-load database with updates
    return record

def get_maintenance_record_by_id(db: Session, maintenance_id: int) -> Optional[MaintenanceRecord]:
    """
    Get maintenance record by ID
    
    Parameters :
        db             : Database session
        maintenance_id : Maintenance record ID 
    Returns :
        record         : MaintenanceRecord object with matching id or none if nothing found
    """
    #Filter for maintenance record where the ids match (first returns the first match or none)
    record = db.query(MaintenanceRecord).filter(MaintenanceRecord.maintenance_id == maintenance_id).first()
    return record

def get_maintenance_by_equipment(db: Session, equipment_id: int) -> List[MaintenanceRecord]:
    """
    Get all maintenance records for a specific equipment

    Parameters :
        db           : Database session
        equipment_id : Equipment ID
    Returns :
        records      : List of MaintenanceRecord objects for that equipment
    """
    #Filter through ALL maintenance records for a specific equipment
    records = db.query(MaintenanceRecord).filter(MaintenanceRecord.equipment_id == equipment_id).all()
    return records

def get_maintenance_by_status(db: Session, status: str) -> List[MaintenanceRecord]:
    """
    Get maintenance records by status (open, in_progress, resolved)

    Parameters :
        db      : Database session
        status  : Maintenance status to filter by
    Returns :
        records : List of MaintenanceRecord objects with that status
    """
    #Filter through ALL maintenance records with a specific status
    records = db.query(MaintenanceRecord).filter(MaintenanceRecord.status == status).all()
    return records

def get_all_maintenance_records(db: Session, skip: int = 0, limit: int = 100) -> List[MaintenanceRecord]:
    """
    Get all maintenance records with pagination

    Parameters :
        db      : Database session
        skip    : Num of records to skip
        limit   : Maximum records to return
    Returns :
        records : List of MaintenanceRecord objects
    """
    #Get every maintenance record object
    records = db.query(MaintenanceRecord).offset(skip).limit(limit).all()
    return records

def update_maintenance_status(db: Session, maintenance_id: int, status: str, resolved_at: Optional[datetime] = None) -> Optional[MaintenanceRecord]:
    """
    Update maintenance record status

    Parameters :
        db             : Database session
        maintenance_id : Maintenance record ID (Record we want to update)
        status         : New status
        resolved_at    : Resolution timestamp (optional)
    Returns :
        record         : Updated MaintenanceRecord object or none if not found
    """
    #get maintenance record by id and if not exists return none
    record = get_maintenance_record_by_id(db, maintenance_id)
    if not record:
        return None
    
    #update status
    record.status = status
    
    #update resolved_at if provided
    if resolved_at is not None:
        record.resolved_at = resolved_at
    
    db.commit()          #save changes to database
    db.refresh(record)   #re-load database with updates
    return record

def delete_maintenance_record(db: Session, maintenance_id: int) -> bool:
    """
    Delete a maintenance record from database

    Parameters :
        db             : Database session
        maintenance_id : Maintenance record ID (Record to delete)
    Returns :
        True           : If deletion successful else, False if not found
    """
    #get maintenance record by id and if not exists return False
    record = get_maintenance_record_by_id(db, maintenance_id)
    if not record:
        return False
    
    db.delete(record)    #delete maintenance record from database
    db.commit()          #save changes to database
    return True