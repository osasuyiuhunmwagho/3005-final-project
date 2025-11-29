"""
Admin service - business logic for administrative operations.
Implements room booking, equipment maintenance tracking, class management, and billing/payment operations.
Coordinates admin-related functionality and resource management.
"""
from sqlalchemy.orm import Session
from repositories import admin_repository, equipment_repository, maintenance_repository, room_repository
from datetime import datetime
from typing import Optional

def report_equipment_issue(db: Session, equipment_id: int, admin_id: int, issue_description: str) -> dict:
    """
    Log issues, track repair status, associate with room/equipment.
    
    Parameters:
        db                : Database session
        equipment_id      : Equipment ID that has the issue
        admin_id          : Admin ID reporting the issue
        issue_description : Description of the problem
    Returns:
        dict with success status, message, and maintenance record
    """
    #Check if equipment exists
    equipment = equipment_repository.get_equipment_by_id(db, equipment_id)
    if not equipment:
        return {"success": False, "message": "Equipment not found"}
    
    #Create maintenance record with status 'open'
    maintenance_record = maintenance_repository.create_maintenance_record(
        db=db,
        equipment_id=equipment_id,
        admin_id=admin_id,
        issue_description=issue_description,
        status="open"
    )
    
    #Update equipment status to 'broken'
    equipment_repository.update_equipment(db, equipment_id, status="broken")
    
    return {
        "success": True,
        "message": f"Maintenance record created for equipment '{equipment.name}'",
        "record": maintenance_record
    }

def resolve_equipment_issue(db: Session, maintenance_id: int) -> dict:
    """
    Mark an equipment issue as resolved.
    
    Parameters:
        db             : Database session
        maintenance_id : Maintenance record ID to resolve
    Returns:
        dict with success status and message
    """
    #Get maintenance record
    record = maintenance_repository.get_maintenance_record_by_id(db, maintenance_id)
    if not record:
        return {"success": False, "message": "Maintenance record not found"}
    
    #Update maintenance status to 'resolved' with current timestamp
    maintenance_repository.update_maintenance_status(
        db=db,
        maintenance_id=maintenance_id,
        status="resolved",
        resolved_at=datetime.now()
    )
    
    #Update equipment status back to 'working'
    equipment_repository.update_equipment(db, record.equipment_id, status="working")
    
    return {
        "success": True,
        "message": "Equipment issue resolved and equipment marked as working"
    }