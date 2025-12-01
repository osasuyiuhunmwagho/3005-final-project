"""
PersonalTrainingSession repository - data access layer for session entities.
Manages session scheduling, retrieval, and status updates.
Handles queries for upcoming/past sessions, sessions by member or trainer.
"""
from sqlalchemy.orm import Session
from model.personal_training_session import PersonalTrainingSession
from model.trainer_availability import TrainerAvailability
from model.group_class import GroupClass

def trainer_available(db: Session, trainer_id: int, start, end):
    """
    Trainer must have an availability window covering the whole session.
    """
    return db.query(TrainerAvailability).filter(
        TrainerAvailability.trainer_id == trainer_id,
        TrainerAvailability.start_time <= start,
        TrainerAvailability.end_time >= end
    ).first() is not None

def trainer_session_conflict(db: Session, trainer_id: int, start, end):
    """Trainer cannot have overlapping PT sessions."""
    return db.query(PersonalTrainingSession).filter(
        PersonalTrainingSession.trainer_id == trainer_id,
        PersonalTrainingSession.start_time < end,
        PersonalTrainingSession.end_time > start,
        PersonalTrainingSession.status == "scheduled"
    ).first() is not None

def room_conflict(db: Session, room_id: int, start, end):
    """Detect room conflicts with classes or PT sessions."""
    pt_conf = db.query(PersonalTrainingSession).filter(
        PersonalTrainingSession.room_id == room_id,
        PersonalTrainingSession.start_time < end,
        PersonalTrainingSession.end_time > start,
        PersonalTrainingSession.status == "scheduled"
    ).first()

    class_conf = db.query(GroupClass).filter(
        GroupClass.room_id == room_id,
        GroupClass.start_time < end,
        GroupClass.end_time > start
    ).first()

    return pt_conf or class_conf

def create_session(db: Session, session: PersonalTrainingSession):
    """Insert PT session."""
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

