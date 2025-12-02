"""
Model package - contains all database entity models.
Import all models here so SQLAlchemy can discover them for table creation.
"""

# Import all implemented models to ensure they're registered with Base
from app.model.admin_staff import AdminStaff
from app.model.trainer import Trainer
from app.model.member import Member
from app.model.room import Room
from app.model.equipment import Equipment
from app.model.group_class import GroupClass
from app.model.personal_training_session import PersonalTrainingSession
from app.model.trainer_availability import TrainerAvailability
from app.model.maintenance_record import MaintenanceRecord
from app.model.health_metric import HealthMetric
from app.model.fitness_goal import FitnessGoal
from app.model.class_registration import ClassRegistration

__all__ = [
    "AdminStaff",
    "Trainer",
    "Member",
    "Room",
    "Equipment",
    "GroupClass",
    "PersonalTrainingSession",
    "TrainerAvailability",
    "MaintenanceRecord",
    "HealthMetric",
    "FitnessGoal",
    "ClassRegistration",
]
