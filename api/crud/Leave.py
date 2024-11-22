from fastapi import HTTPException
from models.Availability import Availability
from models.User import User
import schema
from .Timezone import *

def get_all():
    """
    Fetch all availability records.

    Returns:
        List[Availability]: A list of all availability records in the database.
    """
    availabilities = Availability.all()
    return availabilities.all()

def add(availability_data: schema.AvailabilityBase):
    """
    Add a new availability record.

    Args:
        availability_data (schema.AvailabilityBase): Data for the new availability record.

    Returns:
        Availability: The created availability record.

    Raises:
        HTTPException: If the user associated with the record is not found.
    """
    user = User.find(availability_data.user_id)
    if not user:
        raise HTTPException(status_code=400, detail="Host not found.")
    
    availability = Availability()
    for attr in vars(availability_data).keys():
        setattr(availability, attr, getattr(availability_data, attr))
    
    availability.save()
    return availability

def get(availability_id: int):
    """
    Fetch a single availability record by its ID.

    Args:
        availability_id (int): The ID of the availability record.

    Returns:
        Availability: The requested availability record.

    Raises:
        HTTPException: If the record is not found.
    """
    availability = Availability.find(availability_id)
    if not availability:
        raise HTTPException(status_code=404, detail="Availability not found.")
    return availability

def availabilitys_by_user(user_id: int):
    """
    Fetch all availability records for a specific user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        List[Availability]: A list of availability records associated with the user.
    """
    availabilities = Availability.where("user_id", user_id).get().all()
    return availabilities
