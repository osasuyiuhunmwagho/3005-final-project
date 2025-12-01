"""
Trainer API routes - REST endpoints for trainer operations.
Exposes HTTP endpoints for setting availability, viewing schedules, and member lookup.
Handles trainer authentication and request processing.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.trainer_schemas import TrainerCreate, TrainerResponse
from schemas.common_schemas import AvailabilityCreate
from model.trainer import Trainer
from model.trainer_availability import TrainerAvailability

import repositories.trainer_repository as trainer_repo
import repositories.trainer_availability_repository as availability_repo

router = APIRouter(prefix="/trainer", tags=["Trainer"])

# -----------------------------
# CREATE TRAINER
# -----------------------------
@router.post("/", response_model=TrainerResponse)
def create_trainer(data: TrainerCreate, db: Session = Depends(get_db)):
    existing = trainer_repo.get_trainer_by_email(db, data.email)
    if existing:
        raise HTTPException(400, "Trainer email already exists")

    trainer = Trainer(**data.dict())
    return trainer_repo.create_trainer(db, trainer)

# -----------------------------
# GET TRAINER
# -----------------------------
@router.get("/{trainer_id}", response_model=TrainerResponse)
def get_trainer(trainer_id: int, db: Session = Depends(get_db)):
    trainer = trainer_repo.get_trainer_by_id(db, trainer_id)
    if not trainer:
        raise HTTPException(404, "Trainer not found")
    return trainer

# -----------------------------
# LIST TRAINERS
# -----------------------------
@router.get("/", response_model=list[TrainerResponse])
def list_trainers(db: Session = Depends(get_db)):
    return trainer_repo.list_trainers(db)

# -----------------------------
# ADD TRAINER AVAILABILITY
# -----------------------------
@router.post("/{trainer_id}/availability")
def add_availability(trainer_id: int, data: AvailabilityCreate, db: Session = Depends(get_db)):

    if availability_repo.has_overlapping_availability(db, trainer_id, data.start_time, data.end_time):
        raise HTTPException(400, "Availability overlaps with existing schedule")

    slot = TrainerAvailability(
        trainer_id=trainer_id,
        start_time=data.start_time,
        end_time=data.end_time
    )
    return availability_repo.create_availability(db, slot)

# -----------------------------
# LIST TRAINER AVAILABILITY
# -----------------------------
@router.get("/{trainer_id}/availability")
def get_availability(trainer_id: int, db: Session = Depends(get_db)):
    return availability_repo.list_availability(db, trainer_id)
