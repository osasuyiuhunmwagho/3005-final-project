"""
Model package - contains all database entity models.
Import all models here so SQLAlchemy can discover them for table creation.
"""

# Import all implemented models to ensure they're registered with Base
from model.admin_staff import AdminStaff
from model.trainer import Trainer
from model.member import Member
from model.room import Room
from model.equipment import Equipment
from model.group_class import GroupClass
from model.personal_training_session import PersonalTrainingSession
from model.trainer_availability import TrainerAvailability
from model.maintenance_record import MaintenanceRecord
from model.health_metric import HealthMetric
from model.fitness_goal import FitnessGoal
from model.class_registration import ClassRegistration

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
