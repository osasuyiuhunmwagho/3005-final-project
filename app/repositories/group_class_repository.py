"""
GroupClass repository - data access layer for GroupClass entities.
Handles CRUD operations for fitness classes.
Manages class schedules, capacity tracking, and class queries.
"""


from sqlalchemy.orm import Session
from app.model.group_class import GroupClass

def create_class(db: Session, new_class: GroupClass):
    """Add new group class."""
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class

def room_conflict(db: Session, room_id: int, start, end):
    """Check if room is booked for other classes."""
    return db.query(GroupClass).filter(
        GroupClass.room_id == room_id,
        GroupClass.start_time < end,
        GroupClass.end_time > start
    ).first() is not None

def trainer_conflict(db: Session, trainer_id: int, start, end):
    """Check if trainer is teaching another class at this time."""
    return db.query(GroupClass).filter(
        GroupClass.trainer_id == trainer_id,
        GroupClass.start_time < end,
        GroupClass.end_time > start
    ).first() is not None
