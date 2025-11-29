"""
Booking service - business logic for scheduling and room management.
Handles conflict detection for room bookings and trainer availability.
Ensures no double-booking of rooms or overlapping trainer schedules.
"""
from sqlalchemy.orm import Session
from repositories import room_repository
from model.group_class import GroupClass
from model.personal_training_session import PersonalTrainingSession
from datetime import datetime
from sqlalchemy import and_, or_

def check_room_availability(db: Session, room_id: int, start_time: datetime, end_time: datetime) -> dict:
    """
    Assign rooms for sessions or classes. Prevent double-booking.
    
    Parameters:
        db         : Database session
        room_id    : Room ID to check
        start_time : Requested start time
        end_time   : Requested end time
    Returns:
        dict with success status and message
    """
    #Check if room exists
    room = room_repository.get_room_by_id(db, room_id)
    if not room:
        return {"success": False, "message": "Room not found"}
    
    #Check for conflicting group classes
    class_conflict = db.query(GroupClass).filter(
        and_(
            GroupClass.room_id == room_id,
            or_(#Time constrants
                #New booking starts during existing class
                and_(GroupClass.start_time <= start_time, GroupClass.end_time > start_time),
                #New booking ends during existing class
                and_(GroupClass.start_time < end_time, GroupClass.end_time >= end_time),
                #New booking completely contains existing class
                and_(GroupClass.start_time >= start_time, GroupClass.end_time <= end_time)
            )
        )
    ).first()
    
    if class_conflict:
        return {"success": False, "message": f"Room is booked for class '{class_conflict.class_name}' during this time"}
    
    #Check for conflicting personal training sessions
    session_conflict = db.query(PersonalTrainingSession).filter(
        and_(
            PersonalTrainingSession.room_id == room_id,
            PersonalTrainingSession.status == 'scheduled',
            or_(
                and_(PersonalTrainingSession.start_time <= start_time, PersonalTrainingSession.end_time > start_time),
                and_(PersonalTrainingSession.start_time < end_time, PersonalTrainingSession.end_time >= end_time),
                and_(PersonalTrainingSession.start_time >= start_time, PersonalTrainingSession.end_time <= end_time)
            )
        )
    ).first()
    
    if session_conflict:
        return {"success": False, "message": "Room is booked for a personal training session during this time"}
    
    return {"success": True, "message": "Room is available"}