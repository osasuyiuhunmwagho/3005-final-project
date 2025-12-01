"""
Trainer repository - data access layer for Trainer entities.
Handles database operations for trainers (CRUD, search by specialization, etc.).
Manages trainer data persistence.
"""

from sqlalchemy.orm import Session
from model.trainer import Trainer

def create_trainer(db: Session, trainer: Trainer):
    """Insert a new trainer into the database."""
    db.add(trainer)
    db.commit()
    db.refresh(trainer)
    return trainer

def get_trainer_by_id(db: Session, trainer_id: int):
    """Fetch trainer using their ID."""
    return db.query(Trainer).filter(Trainer.trainer_id == trainer_id).first()

def get_trainer_by_email(db: Session, email: str):
    """Check if trainer email already exists."""
    return db.query(Trainer).filter(Trainer.email == email).first()

def list_trainers(db: Session):
    """Return a list of all trainers."""
    return db.query(Trainer).all()


