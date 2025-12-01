"""
Member API routes - REST endpoints for member operations.
Exposes HTTP endpoints for member registration, profile updates, health metrics, dashboard, and class registration.
Handles request validation and response formatting for member-facing features.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from typing import List

from core.database import get_db
from schemas.member_schemas import (
    MemberCreate, MemberUpdate, MemberResponse,
    HealthMetricCreate, HealthMetricResponse,
    ClassRegistrationCreate, ClassRegistrationResponse,
    FitnessGoalCreate, FitnessGoalUpdate, FitnessGoalResponse
)
from model.member import Member
from model.health_metric import HealthMetric
from model.class_registration import ClassRegistration
from model.fitness_goal import FitnessGoal
from model.group_class import GroupClass
import repositories.member_repository as member_repo
import repositories.health_metric_repository as health_metric_repo
import repositories.class_registration_repository as class_registration_repo
import repositories.fitness_goal_repository as fitness_goal_repo
import repositories.group_class_repository as group_class_repo

router = APIRouter(prefix="/member", tags=["Member"])

# -----------------------------
# CREATE MEMBER
# -----------------------------
@router.post("/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    """Create a new member"""
    try:
        # Check if email already exists
        existing = member_repo.get_member_by_email(db, member.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        new_member = Member(**member.dict())
        return member_repo.create_member(db, new_member)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error. Email may already exist."
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )

# -----------------------------
# GET MEMBER BY ID
# -----------------------------
@router.get("/{member_id}", response_model=MemberResponse)
def get_member(member_id: int, db: Session = Depends(get_db)):
    """Get member by ID"""
    try:
        member = member_repo.get_member_by_id(db, member_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found"
            )
        return member
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

# -----------------------------
# GET MEMBER BY EMAIL
# -----------------------------
@router.get("/email/{email}", response_model=MemberResponse)
def get_member_by_email(email: str, db: Session = Depends(get_db)):
    """Get member by email address"""
    try:
        member = member_repo.get_member_by_email(db, email)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found"
            )
        return member
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

# -----------------------------
# LIST ALL MEMBERS
# -----------------------------
@router.get("/", response_model=List[MemberResponse])
def list_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all members with pagination"""
    try:
        return member_repo.get_all_members(db, skip=skip, limit=limit)
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection error. Please check your database configuration in .env file."
        )
    except SQLAlchemyError as e:
        error_msg = str(e)
        if "no password supplied" in error_msg or "connection" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection failed. Please configure your database credentials in .env file."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {error_msg}"
        )

# -----------------------------
# UPDATE MEMBER
# -----------------------------
@router.put("/{member_id}", response_model=MemberResponse)
def update_member(member_id: int, member_update: MemberUpdate, db: Session = Depends(get_db)):
    """Update member information"""
    try:
        # Check if email is being changed and verify uniqueness
        if member_update.email:
            existing = member_repo.get_member_by_email(db, member_update.email)
            if existing and existing.member_id != member_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered to another member"
                )
        
        updated = member_repo.update_member(
            db, 
            member_id,
            name=member_update.name,
            email=member_update.email,
            date_of_birth=member_update.date_of_birth,
            gender=member_update.gender,
            phone=member_update.phone
        )
        
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found"
            )
        return updated
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error"
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

# -----------------------------
# DELETE MEMBER
# -----------------------------
@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id: int, db: Session = Depends(get_db)):
    """Delete a member"""
    try:
        success = member_repo.delete_member(db, member_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found"
            )
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

# -----------------------------
# HEALTH METRIC ENDPOINTS
# -----------------------------

@router.post("/{member_id}/health-metrics", response_model=HealthMetricResponse, status_code=status.HTTP_201_CREATED)
def create_health_metric(member_id: int, health_metric: HealthMetricCreate, db: Session = Depends(get_db)):
    """Record a new health metric for a member"""
    try:
        # Verify member exists
        member = member_repo.get_member_by_id(db, member_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found"
            )
        
        # Ensure member_id matches
        if health_metric.member_id != member_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Member ID in URL must match member_id in request body"
            )
        
        new_metric = HealthMetric(**health_metric.dict())
        return health_metric_repo.create_health_metric(db, new_metric)
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error"
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.get("/{member_id}/health-metrics", response_model=List[HealthMetricResponse])
def get_member_health_metrics(member_id: int, limit: int = 100, db: Session = Depends(get_db)):
    """Get all health metrics for a member, ordered by most recent first"""
    try:
        # Verify member exists
        member = member_repo.get_member_by_id(db, member_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found"
            )
        
        return health_metric_repo.get_health_metrics_by_member(db, member_id, limit=limit)
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.get("/{member_id}/health-metrics/latest", response_model=HealthMetricResponse)
def get_latest_health_metric(member_id: int, db: Session = Depends(get_db)):
    """Get the most recent health metric for a member"""
    try:
        # Verify member exists
        member = member_repo.get_member_by_id(db, member_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found"
            )
        
        metric = health_metric_repo.get_latest_health_metric(db, member_id)
        if not metric:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No health metrics found for this member"
            )
        return metric
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.get("/health-metrics/{metric_id}", response_model=HealthMetricResponse)
def get_health_metric(metric_id: int, db: Session = Depends(get_db)):
    """Get a specific health metric by ID"""
    try:
        metric = health_metric_repo.get_health_metric_by_id(db, metric_id)
        if not metric:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Health metric not found"
            )
        return metric
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.delete("/health-metrics/{metric_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_health_metric(metric_id: int, db: Session = Depends(get_db)):
    """Delete a health metric entry"""
    try:
        success = health_metric_repo.delete_health_metric(db, metric_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Health metric not found"
            )
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

# -----------------------------
# CLASS REGISTRATION ENDPOINTS
# -----------------------------

@router.post("/{member_id}/class-registrations", response_model=ClassRegistrationResponse, status_code=status.HTTP_201_CREATED)
def register_for_class(member_id: int, registration: ClassRegistrationCreate, db: Session = Depends(get_db)):
    """Register a member for a group class"""
    try:
        # Verify member exists
        member = member_repo.get_member_by_id(db, member_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found"
            )
        
        # Ensure member_id matches
        if registration.member_id != member_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Member ID in URL must match member_id in request body"
            )
        
        # Verify class exists
        group_class = db.query(GroupClass).filter(GroupClass.class_id == registration.class_id).first()
        if not group_class:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group class not found"
            )
        
        # Check if already registered
        existing = class_registration_repo.get_registration_by_member_and_class(
            db, member_id, registration.class_id
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Member is already registered for this class"
            )
        
        # Check capacity
        current_registrations = class_registration_repo.get_class_registration_count(
            db, registration.class_id
        )
        if current_registrations >= group_class.capacity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Class is at full capacity"
            )
        
        new_registration = ClassRegistration(**registration.dict())
        return class_registration_repo.create_registration(db, new_registration)
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error"
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.get("/{member_id}/class-registrations", response_model=List[ClassRegistrationResponse])
def get_member_class_registrations(member_id: int, db: Session = Depends(get_db)):
    """Get all class registrations for a member"""
    try:
        # Verify member exists
        member = member_repo.get_member_by_id(db, member_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found"
            )
        
        return class_registration_repo.get_registrations_by_member(db, member_id)
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.delete("/{member_id}/class-registrations/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_class_registration(member_id: int, class_id: int, db: Session = Depends(get_db)):
    """Cancel a member's registration for a class"""
    try:
        success = class_registration_repo.delete_registration_by_member_and_class(
            db, member_id, class_id
        )
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registration not found"
            )
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

# -----------------------------
# FITNESS GOAL ENDPOINTS
# -----------------------------

@router.post("/{member_id}/fitness-goals", response_model=FitnessGoalResponse, status_code=status.HTTP_201_CREATED)
def create_fitness_goal(member_id: int, goal: FitnessGoalCreate, db: Session = Depends(get_db)):
    """Create a new fitness goal for a member"""
    try:
        # Verify member exists
        member = member_repo.get_member_by_id(db, member_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found"
            )
        
        # Ensure member_id matches
        if goal.member_id != member_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Member ID in URL must match member_id in request body"
            )
        
        new_goal = FitnessGoal(**goal.dict())
        return fitness_goal_repo.create_fitness_goal(db, new_goal)
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error"
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.get("/{member_id}/fitness-goals", response_model=List[FitnessGoalResponse])
def get_member_fitness_goals(member_id: int, active_only: bool = False, db: Session = Depends(get_db)):
    """Get all fitness goals for a member"""
    try:
        # Verify member exists
        member = member_repo.get_member_by_id(db, member_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found"
            )
        
        return fitness_goal_repo.get_goals_by_member(db, member_id, active_only=active_only)
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.get("/{member_id}/fitness-goals/active", response_model=List[FitnessGoalResponse])
def get_active_fitness_goals(member_id: int, db: Session = Depends(get_db)):
    """Get all active fitness goals for a member"""
    try:
        # Verify member exists
        member = member_repo.get_member_by_id(db, member_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found"
            )
        
        return fitness_goal_repo.get_active_goals_by_member(db, member_id)
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.get("/fitness-goals/{goal_id}", response_model=FitnessGoalResponse)
def get_fitness_goal(goal_id: int, db: Session = Depends(get_db)):
    """Get a specific fitness goal by ID"""
    try:
        goal = fitness_goal_repo.get_goal_by_id(db, goal_id)
        if not goal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fitness goal not found"
            )
        return goal
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.put("/fitness-goals/{goal_id}", response_model=FitnessGoalResponse)
def update_fitness_goal(goal_id: int, goal_update: FitnessGoalUpdate, db: Session = Depends(get_db)):
    """Update a fitness goal"""
    try:
        updated = fitness_goal_repo.update_goal(
            db,
            goal_id,
            goal_type=goal_update.goal_type,
            target_value=goal_update.target_value,
            current_value=goal_update.current_value,
            target_date=goal_update.target_date,
            is_active=goal_update.is_active
        )
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fitness goal not found"
            )
        return updated
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.delete("/fitness-goals/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fitness_goal(goal_id: int, db: Session = Depends(get_db)):
    """Delete a fitness goal"""
    try:
        success = fitness_goal_repo.delete_goal(db, goal_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fitness goal not found"
            )
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
