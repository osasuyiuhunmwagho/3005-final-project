"""
ClassRegistration repository - data access layer for class registrations.
Handles member enrollment in group classes.
Manages registration creation, cancellation, and capacity checks.
"""

from sqlalchemy.orm import Session
from model.class_registration import ClassRegistration
from model.group_class import GroupClass
from typing import Optional, List

def create_registration(db: Session, registration: ClassRegistration) -> ClassRegistration:
    """Create a new class registration."""
    db.add(registration)
    db.commit()
    db.refresh(registration)
    return registration

def get_registration_by_id(db: Session, registration_id: int) -> Optional[ClassRegistration]:
    """Get registration by ID."""
    return db.query(ClassRegistration).filter(
        ClassRegistration.registration_id == registration_id
    ).first()

def get_registrations_by_member(db: Session, member_id: int) -> List[ClassRegistration]:
    """Get all class registrations for a member."""
    return db.query(ClassRegistration).filter(
        ClassRegistration.member_id == member_id
    ).all()

def get_registrations_by_class(db: Session, class_id: int) -> List[ClassRegistration]:
    """Get all registrations for a specific class."""
    return db.query(ClassRegistration).filter(
        ClassRegistration.class_id == class_id
    ).all()

def get_registration_by_member_and_class(
    db: Session, member_id: int, class_id: int
) -> Optional[ClassRegistration]:
    """Check if a member is already registered for a class."""
    return db.query(ClassRegistration).filter(
        ClassRegistration.member_id == member_id,
        ClassRegistration.class_id == class_id
    ).first()

def get_class_registration_count(db: Session, class_id: int) -> int:
    """Get the number of registrations for a class (for capacity checking)."""
    return db.query(ClassRegistration).filter(
        ClassRegistration.class_id == class_id
    ).count()

def delete_registration(db: Session, registration_id: int) -> bool:
    """Cancel/delete a class registration."""
    registration = get_registration_by_id(db, registration_id)
    if not registration:
        return False
    
    db.delete(registration)
    db.commit()
    return True

def delete_registration_by_member_and_class(
    db: Session, member_id: int, class_id: int
) -> bool:
    """Cancel a registration by member and class."""
    registration = get_registration_by_member_and_class(db, member_id, class_id)
    if not registration:
        return False
    
    db.delete(registration)
    db.commit()
    return True
