"""
Common schemas - shared data structures across the application.
Defines reusable schemas for responses, pagination, error handling, and common entities.
Reduces code duplication and ensures consistent API responses.
"""

from pydantic import BaseModel
from datetime import datetime

class AvailabilityCreate(BaseModel):
    start_time: datetime
    end_time: datetime


