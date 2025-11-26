"""
Admin repository - data access layer for AdminStaff entities.
Handles database operations for administrative staff.
Manages admin user data and authentication.
"""
from sqlalchemy.orm import Session
from model.admin_staff import AdminStaff
from typing import Optional, List

def create_admin(db: Session, name:str, email:str, role:str) -> AdminStaff:
    """
    Create a new admin staff instance for database

    Parameters :
        db    : Database session
        name  : Admin name
        email : Admin email (Unique)
        role  : Admin role (example: manager, receptionist, ect)
    Returns :
        admin : Created AdminStaff object
    """
    admin = AdminStaff(
        name = name,
        email = email,
        role = role
    )
    db.add(admin)       #add to database
    db.commit()         #save changes to database
    db.refresh(admin)   #re-load database with updates
    return admin

def get_admin_by_id(db: Session, id: int) -> Optional[AdminStaff]:
    """
    Get admin by ID
    
    Parameters :
        db : Database session
        id : Admin ID 
    Returns :
        admin    : AdminStaff object with matching id or none if nothing found
    """
    #Filter for admin staff where the ids match (first returns the first match or none)
    admin = db.query(AdminStaff).filter(AdminStaff.admin_id == id).first()
    return admin

def get_admin_by_email(db: Session, email: str) -> Optional[AdminStaff]:
    """
    Get admin by email (for logins and authentication)

    Parameters :
        db    : Database session
        email : Admin Email 
    Returns :
        admin : AdminStaff object with matching email or none if nothing found 
    """
    #Filter for admin staff where the emails match (first returns the first match or none)
    admin = db.query(AdminStaff).filter(AdminStaff.email == email).first()
    return admin

def get_all_admins(db: Session, skip: int = 0, limit: int = 100) -> List[AdminStaff]:
    """
    Get all admins with pagination

    Parameters :
        db     : Database session
        skip   : Num of records to skip
        limit  : Maximum records to return
    Returns :
        admins : List of AdminStaff objects
    """
    #Get every admin object
    admins = db.query(AdminStaff).offset(skip).limit(limit).all()
    return admins

def update_admin(db: Session, id: int, name: Optional[str] = None, email: Optional[str] = None, role: Optional[str] = None) -> Optional[AdminStaff]:
    """
    Update information for an Admin

    Parameters :
        db    : Database session
        id    : Admin ID (Admin we want to upodate)
        name  : New name (optional)
        email : New email (optional) 
        role  : New role (optional)
    Returns :
        admin : Updated AdminStaff object or none if not found
    """
    #get admin by id and if not exists return none
    admin = get_admin_by_id(db, id)
    if not admin:
        return None
    
    #update features if not none
    if name is not None:
        admin.name = name
    if email is not None:
        admin.email = email
    if role is not None:
        admin.role = role
    
    db.commit()             #save changes to database
    db.refresh(admin)       #re-load database with updates
    return admin

def delete_admin(db: Session, id: int) -> bool:
    """
    Delete an admin from database

    Parameters :
        db   : Database session
        id   : Admin ID (Admin to delete)
    Returns :
        True : If deletion successful else, False if not found
    """
    #get admin by id and if not exists return False
    admin = get_admin_by_id(db, id)
    if not admin:
        return False
    
    db.delete(admin)    #delete admin from database
    db.commit()         #save changes to database
    return True