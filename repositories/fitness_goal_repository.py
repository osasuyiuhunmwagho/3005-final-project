"""
FitnessGoal repository - data access layer for FitnessGoal entities.
Handles CRUD operations for member fitness goals.
Queries active goals, goals by member, and goal history.
"""

from sqlalchemy.orm import Session
from model.fitness_goal import FitnessGoal
from typing import Optional, List
from datetime import date

def create_fitness_goal(db: Session, goal: FitnessGoal) -> FitnessGoal:
    """Create a new fitness goal."""
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal

def get_goal_by_id(db: Session, goal_id: int) -> Optional[FitnessGoal]:
    """Get fitness goal by ID."""
    return db.query(FitnessGoal).filter(FitnessGoal.goal_id == goal_id).first()

def get_goals_by_member(db: Session, member_id: int, active_only: bool = False) -> List[FitnessGoal]:
    """Get all fitness goals for a member."""
    query = db.query(FitnessGoal).filter(FitnessGoal.member_id == member_id)
    if active_only:
        query = query.filter(FitnessGoal.is_active == True)
    return query.order_by(FitnessGoal.created_at.desc()).all()

def get_active_goals_by_member(db: Session, member_id: int) -> List[FitnessGoal]:
    """Get all active fitness goals for a member."""
    return get_goals_by_member(db, member_id, active_only=True)

def update_goal(
    db: Session,
    goal_id: int,
    goal_type: Optional[str] = None,
    target_value: Optional[float] = None,
    current_value: Optional[float] = None,
    target_date: Optional[date] = None,
    is_active: Optional[bool] = None
) -> Optional[FitnessGoal]:
    """Update a fitness goal."""
    goal = get_goal_by_id(db, goal_id)
    if not goal:
        return None
    
    if goal_type is not None:
        goal.goal_type = goal_type
    if target_value is not None:
        goal.target_value = target_value
    if current_value is not None:
        goal.current_value = current_value
    if target_date is not None:
        goal.target_date = target_date
    if is_active is not None:
        goal.is_active = is_active
    
    db.commit()
    db.refresh(goal)
    return goal

def delete_goal(db: Session, goal_id: int) -> bool:
    """Delete a fitness goal."""
    goal = get_goal_by_id(db, goal_id)
    if not goal:
        return False
    
    db.delete(goal)
    db.commit()
    return True
