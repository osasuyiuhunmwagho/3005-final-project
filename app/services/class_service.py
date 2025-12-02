"""
Class service - business logic for group class operations.
Manages class registration, capacity checking, and enrollment operations.
Handles member registration for classes and capacity validation.
"""
from sqlalchemy.orm import Session
from app.repositories import group_class_repository
from app.model.group_class import GroupClass
from app.services import booking_service
from datetime import datetime

def create_group_class(db: Session, class_name: str, trainer_id: int, room_id: int, admin_id: int, start_time: datetime, end_time: datetime, capacity: int) -> dict:
    """
    Create a new group class with room availability validation.
    
    Parameters:
        db         : Database session
        class_name : Name of the class
        trainer_id : Trainer ID assigned to the class
        room_id    : Room ID where class will be held
        admin_id   : Admin ID who is creating the class
        start_time : Class start time
        end_time   : Class end time
        capacity   : Maximum number of members allowed
    Returns:
        dict with success status, message, and class object if successful
    """
    #Check if room is available for the requested time slot
    availability = booking_service.check_room_availability(db, room_id, start_time, end_time)
    if not availability["success"]:
        return availability     #Error message from booking service
    
    #Create the group class
    new_class = group_class_repository.create_group_class(
        db=db,
        class_name=class_name,
        trainer_id=trainer_id,
        room_id=room_id,
        admin_id=admin_id,
        start_time=start_time,
        end_time=end_time,
        capacity=capacity
    )
    
    return {
        "success": True,
        "message": f"Group class '{class_name}' created successfully",
        "class": new_class
    }
