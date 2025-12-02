"""
Trainer service - business logic for trainer operations.
Implements trainer availability management, schedule viewing, and member lookup.
Coordinates trainer-related business rules and data access.
"""
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.model.trainer import Trainer
from app.model.trainer_availability import TrainerAvailability
import app.repositories.trainer_repository as trainer_repo
import app.repositories.trainer_availability_repository as availability_repo
import app.repositories.member_repository as member_repo


def set_availability(
    db: Session,
    trainer_id: int,
    start_time: datetime,
    end_time: datetime
) -> Dict[str, Any]:
    """
    Set availability for a trainer.
    
    Returns:
        dict with success status and availability data
    """
    # Verify trainer exists
    trainer = trainer_repo.get_trainer_by_id(db, trainer_id)
    if not trainer:
        return {
            "success": False,
            "message": "Trainer not found",
            "availability": None
        }
    
    # Check for overlapping availability
    if availability_repo.has_overlapping_availability(db, trainer_id, start_time, end_time):
        return {
            "success": False,
            "message": "Availability overlaps with existing schedule",
            "availability": None
        }
    
    # Validate time range
    if end_time <= start_time:
        return {
            "success": False,
            "message": "End time must be after start time",
            "availability": None
        }
    
    # Create availability slot
    slot = TrainerAvailability(
        trainer_id=trainer_id,
        start_time=start_time,
        end_time=end_time
    )
    
    saved = availability_repo.create_availability(db, slot)
    return {
        "success": True,
        "message": "Availability set successfully",
        "availability": saved
    }


def get_trainer_schedule(db: Session, trainer_id: int) -> Dict[str, Any]:
    """
    Get the full schedule for a trainer including availability slots.
    
    Returns:
        dict with trainer info and schedule data
    """
    trainer = trainer_repo.get_trainer_by_id(db, trainer_id)
    if not trainer:
        return {
            "success": False,
            "message": "Trainer not found",
            "data": None
        }
    
    availability = availability_repo.list_availability(db, trainer_id)
    
    return {
        "success": True,
        "message": "Schedule retrieved",
        "data": {
            "trainer": trainer,
            "availability_slots": availability,
            "total_slots": len(availability)
        }
    }


def check_trainer_available(
    db: Session,
    trainer_id: int,
    start_time: datetime,
    end_time: datetime
) -> Dict[str, Any]:
    """
    Check if a trainer is available during a specific time slot.
    
    Returns:
        dict with availability status
    """
    trainer = trainer_repo.get_trainer_by_id(db, trainer_id)
    if not trainer:
        return {
            "success": False,
            "message": "Trainer not found",
            "available": False
        }
    
    # Check if trainer has availability covering this time
    availability = availability_repo.list_availability(db, trainer_id)
    
    is_available = False
    for slot in availability:
        if slot.start_time <= start_time and slot.end_time >= end_time:
            is_available = True
            break
    
    return {
        "success": True,
        "message": "Available" if is_available else "Not available during this time",
        "available": is_available
    }


def lookup_member(db: Session, member_id: int) -> Dict[str, Any]:
    """
    Look up a member's information (for trainers to view their clients).
    
    Returns:
        dict with member data
    """
    member = member_repo.get_member_by_id(db, member_id)
    if not member:
        return {
            "success": False,
            "message": "Member not found",
            "member": None
        }
    
    return {
        "success": True,
        "message": "Member found",
        "member": member
    }


def get_all_members(db: Session, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
    """
    Get all members (for trainer to see potential clients).
    
    Returns:
        dict with list of members
    """
    members = member_repo.get_all_members(db, skip, limit)
    
    return {
        "success": True,
        "message": f"Found {len(members)} members",
        "members": members,
        "count": len(members)
    }


