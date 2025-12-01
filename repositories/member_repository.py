"""
Member repository - data access layer for Member entities.
Handles all database operations for members (CRUD operations, queries by email, etc.).
Abstracts database logic from business services.
"""

from sqlalchemy.orm import Session
from model.member import Member
from typing import Optional, List
from datetime import date

def create_member(db: Session, member: Member) -> Member:
    """Create a new member in the database."""
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

def get_member_by_id(db: Session, member_id: int) -> Optional[Member]:
    """Get member by ID."""
    return db.query(Member).filter(Member.member_id == member_id).first()

def get_member_by_email(db: Session, email: str) -> Optional[Member]:
    """Get member by email address."""
    return db.query(Member).filter(Member.email == email).first()

def get_all_members(db: Session, skip: int = 0, limit: int = 100) -> List[Member]:
    """Get all members with pagination."""
    return db.query(Member).offset(skip).limit(limit).all()

def update_member(
    db: Session, 
    member_id: int, 
    name: Optional[str] = None,
    email: Optional[str] = None,
    date_of_birth: Optional[date] = None,
    gender: Optional[str] = None,
    phone: Optional[str] = None
) -> Optional[Member]:
    """Update member information."""
    member = get_member_by_id(db, member_id)
    if not member:
        return None
    
    if name is not None:
        member.name = name
    if email is not None:
        member.email = email
    if date_of_birth is not None:
        member.date_of_birth = date_of_birth
    if gender is not None:
        member.gender = gender
    if phone is not None:
        member.phone = phone
    
    db.commit()
    db.refresh(member)
    return member

def delete_member(db: Session, member_id: int) -> bool:
    """Delete a member."""
    member = get_member_by_id(db, member_id)
    if not member:
        return False
    
    db.delete(member)
    db.commit()
    return True
