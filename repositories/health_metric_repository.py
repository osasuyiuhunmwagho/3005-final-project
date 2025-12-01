"""
HealthMetric repository - data access layer for HealthMetric entities.
Handles creation and retrieval of historical health metric entries.
Never overwrites data - all entries are preserved with timestamps.
"""

from sqlalchemy.orm import Session
from model.health_metric import HealthMetric
from typing import Optional, List

def create_health_metric(db: Session, health_metric: HealthMetric) -> HealthMetric:
    """Create a new health metric entry."""
    db.add(health_metric)
    db.commit()
    db.refresh(health_metric)
    return health_metric

def get_health_metric_by_id(db: Session, metric_id: int) -> Optional[HealthMetric]:
    """Get health metric by ID."""
    return db.query(HealthMetric).filter(HealthMetric.metric_id == metric_id).first()

def get_health_metrics_by_member(db: Session, member_id: int, limit: int = 100) -> List[HealthMetric]:
    """Get all health metrics for a specific member, ordered by most recent first."""
    return db.query(HealthMetric).filter(
        HealthMetric.member_id == member_id
    ).order_by(HealthMetric.recorded_at.desc()).limit(limit).all()

def get_latest_health_metric(db: Session, member_id: int) -> Optional[HealthMetric]:
    """Get the most recent health metric for a member."""
    return db.query(HealthMetric).filter(
        HealthMetric.member_id == member_id
    ).order_by(HealthMetric.recorded_at.desc()).first()

def get_all_health_metrics(db: Session, skip: int = 0, limit: int = 100) -> List[HealthMetric]:
    """Get all health metrics with pagination."""
    return db.query(HealthMetric).offset(skip).limit(limit).all()

def delete_health_metric(db: Session, metric_id: int) -> bool:
    """Delete a health metric entry."""
    metric = get_health_metric_by_id(db, metric_id)
    if not metric:
        return False
    
    db.delete(metric)
    db.commit()
    return True
