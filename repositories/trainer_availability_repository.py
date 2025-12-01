"""
TrainerAvailability repository - data access layer for trainer availability.
Manages trainer time slot definitions.
Handles availability queries, overlap detection, and scheduling conflicts.
"""

from sqlalchemy.orm import Session
from model.trainer_availability import TrainerAvailability

def has_overlapping_availability(db: Session, trainer_id: int, start, end):
    """
    Check if trainer already has overlapping availability.
    """
    return db.query(TrainerAvailability).filter(
        TrainerAvailability.trainer_id == trainer_id,
        TrainerAvailability.start_time < end,
        TrainerAvailability.end_time > start
    ).first() is not None

def create_availability(db: Session, availability: TrainerAvailability):
    """Insert availability into DB."""
    db.add(availability)
    db.commit()
    db.refresh(availability)
    return availability

def list_availability(db: Session, trainer_id: int):
    """List all availability slots for a trainer."""
    return db.query(TrainerAvailability).filter(
        TrainerAvailability.trainer_id == trainer_id
    ).all()


