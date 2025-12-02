"""
Member service - business logic for member operations.
Implements member registration, profile management, health metric logging, and dashboard functionality.
Coordinates between repositories to provide high-level member features.
"""
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from datetime import date

from app.model.member import Member
from app.model.health_metric import HealthMetric
from app.model.fitness_goal import FitnessGoal
from app.model.class_registration import ClassRegistration
import app.repositories.member_repository as member_repo
import app.repositories.health_metric_repository as health_metric_repo
import app.repositories.fitness_goal_repository as fitness_goal_repo
import app.repositories.class_registration_repository as class_registration_repo


def register_member(
    db: Session,
    name: str,
    email: str,
    date_of_birth: Optional[date] = None,
    gender: Optional[str] = None,
    phone: Optional[str] = None
) -> Dict[str, Any]:
    """
    Register a new member with validation.
    
    Returns:
        dict with success status, message, and member data
    """
    # Check if email already exists
    existing = member_repo.get_member_by_email(db, email)
    if existing:
        return {
            "success": False,
            "message": "Email already registered",
            "member": None
        }
    
    # Create new member
    new_member = Member(
        name=name,
        email=email,
        date_of_birth=date_of_birth,
        gender=gender,
        phone=phone
    )
    
    member = member_repo.create_member(db, new_member)
    return {
        "success": True,
        "message": "Member registered successfully",
        "member": member
    }


def update_member_profile(
    db: Session,
    member_id: int,
    name: Optional[str] = None,
    email: Optional[str] = None,
    date_of_birth: Optional[date] = None,
    gender: Optional[str] = None,
    phone: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update member profile information.
    
    Returns:
        dict with success status and updated member data
    """
    # Check if member exists
    member = member_repo.get_member_by_id(db, member_id)
    if not member:
        return {
            "success": False,
            "message": "Member not found",
            "member": None
        }
    
    # If changing email, check uniqueness
    if email and email != member.email:
        existing = member_repo.get_member_by_email(db, email)
        if existing:
            return {
                "success": False,
                "message": "Email already in use by another member",
                "member": None
            }
    
    updated = member_repo.update_member(
        db, member_id, name, email, date_of_birth, gender, phone
    )
    
    return {
        "success": True,
        "message": "Profile updated successfully",
        "member": updated
    }


def log_health_metric(
    db: Session,
    member_id: int,
    weight: Optional[float] = None,
    heart_rate: Optional[int] = None,
    body_fat: Optional[float] = None
) -> Dict[str, Any]:
    """
    Log a new health metric for a member.
    
    Returns:
        dict with success status and metric data
    """
    # Verify member exists
    member = member_repo.get_member_by_id(db, member_id)
    if not member:
        return {
            "success": False,
            "message": "Member not found",
            "metric": None
        }
    
    # Create health metric
    metric = HealthMetric(
        member_id=member_id,
        weight=weight,
        heart_rate=heart_rate,
        body_fat=body_fat
    )
    
    saved_metric = health_metric_repo.create_health_metric(db, metric)
    return {
        "success": True,
        "message": "Health metric logged successfully",
        "metric": saved_metric
    }


def get_member_dashboard(db: Session, member_id: int) -> Dict[str, Any]:
    """
    Get dashboard data for a member including profile, health metrics, 
    fitness goals, and class registrations.
    
    Returns:
        dict with all dashboard data
    """
    member = member_repo.get_member_by_id(db, member_id)
    if not member:
        return {
            "success": False,
            "message": "Member not found",
            "data": None
        }
    
    # Get latest health metrics
    health_metrics = health_metric_repo.get_health_metrics_by_member(db, member_id)
    latest_metric = health_metrics[0] if health_metrics else None
    
    # Get active fitness goals
    fitness_goals = fitness_goal_repo.get_goals_by_member(db, member_id)
    active_goals = [g for g in fitness_goals if g.is_active]
    
    # Get class registrations
    registrations = class_registration_repo.get_registrations_by_member(db, member_id)
    
    return {
        "success": True,
        "message": "Dashboard data retrieved",
        "data": {
            "member": member,
            "latest_health_metric": latest_metric,
            "health_metrics_count": len(health_metrics),
            "active_fitness_goals": active_goals,
            "total_goals": len(fitness_goals),
            "class_registrations": registrations,
            "classes_registered": len(registrations)
        }
    }


def set_fitness_goal(
    db: Session,
    member_id: int,
    goal_type: str,
    target_value: float,
    target_date: Optional[date] = None
) -> Dict[str, Any]:
    """
    Set a new fitness goal for a member.
    
    Returns:
        dict with success status and goal data
    """
    member = member_repo.get_member_by_id(db, member_id)
    if not member:
        return {
            "success": False,
            "message": "Member not found",
            "goal": None
        }
    
    goal = FitnessGoal(
        member_id=member_id,
        goal_type=goal_type,
        target_value=target_value,
        current_value=0,
        target_date=target_date,
        is_active=True
    )
    
    saved_goal = fitness_goal_repo.create_goal(db, goal)
    return {
        "success": True,
        "message": "Fitness goal set successfully",
        "goal": saved_goal
    }


def update_goal_progress(
    db: Session,
    goal_id: int,
    current_value: float
) -> Dict[str, Any]:
    """
    Update the progress on a fitness goal.
    
    Returns:
        dict with success status and updated goal
    """
    goal = fitness_goal_repo.get_goal_by_id(db, goal_id)
    if not goal:
        return {
            "success": False,
            "message": "Goal not found",
            "goal": None
        }
    
    updated = fitness_goal_repo.update_goal(db, goal_id, current_value=current_value)
    
    # Check if goal is achieved
    achieved = updated.current_value >= updated.target_value if updated.target_value else False
    
    return {
        "success": True,
        "message": "Goal achieved!" if achieved else "Progress updated",
        "goal": updated,
        "achieved": achieved
    }


