"""
Room repository - data access layer for Room entities.
Handles room data operations and availability queries.
Manages room information for booking purposes.
"""
from sqlalchemy.orm import Session
from model.room import Room
from typing import Optional, List

def create_room(db: Session, room_name: str, capacity: int, location: str, admin_id: int) -> Room:
    """
    Create a new room instance for database

    Parameters :
        db       : Database session
        admin_id : admin id of whoever manages room
        room_name: room name
        capacity : room capacity
        location : room location
    Returns :
        room     : Created Room object
    """
    room = Room(
        room_name = room_name,
        capacity = capacity,
        location = location,
        admin_id = admin_id
    )
    db.add(room)        #add to database
    db.commit()         #save changes to database
    db.refresh(room)    #re-load database with updates
    return room

def get_room_by_id(db: Session, room_id: int) -> Optional[Room]:
    """
    Get room by ID
    
    Parameters :
        db      : Database session
        room_id : Room ID 
    Returns :
        room    : Room object with matching id or none if nothing found
    """
    #Filter for room where the room_ids match (first returns the first match or none)
    room = db.query(Room).filter(Room.room_id == room_id).first()
    return room

def get_all_rooms(db: Session, skip: int = 0, limit: int = 100) -> List[Room]:
    """
    Get all rooms with pagination

    Parameters :
        db     : Database session
        skip   : Number of records to skip
        limit  : Maximum records to return
    Returns :
        rooms  : List of Room objects
    """
    rooms = db.query(Room).offset(skip).limit(limit).all()
    return rooms

def get_rooms_by_capacity(db: Session, min_capacity: int) -> List[Room]:
    """
    Get rooms with at least specified capacity

    Parameters :
        db           : Database session
        min_capacity : Minimum capacity required for a room
    Returns :
        room         : List of room with at least that capcity
    """
    #filter through ALL rooms that have a larger than or equal to min capcity
    room = db.query(Room).filter(Room.capacity >= min_capacity).all()
    return room

def update_room(db: Session, room_id: int, room_name: Optional[str] = None, capacity: Optional[int] = None, location: Optional[str] = None) -> Optional[Room]:
    """
    Update room information

    Parameters :
        db       : Database session
        room_id  : Room ID (Room we want to upodate)
        capacity : New capacity (optional)
        location : New location (optional) 
    Returns :
        room     : Updated Room object or none if not found
    """
    #get room by id and if not exists return none
    room = get_room_by_id(db, room_id)
    if not room:
        return None
    
    #update features if not none
    if room_name is not None:
        room.room_name = room_name
    if capacity is not None:
        room.capacity = capacity
    if location is not None:
        room.location = location
    
    db.commit()             #save changes to database
    db.refresh(room)        #re-load database with updates
    return room

def delete_room(db: Session, id: int) -> bool:
    """
    Delete a room from database

    Parameters :
        db   : Database session
        id   : Admin ID (Admin to delete)
    Returns :
        True : If deletion successful else, False if not found
    """
    #get room by id and if not exists return False
    room = get_room_by_id(db, id)
    if not room:
        return False
    
    db.delete(room)     #delete room from database
    db.commit()         #save changes to database
    return True 