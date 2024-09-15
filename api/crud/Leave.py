from fastapi import HTTPException
from models.Availability import Availability
from models.User import User
import schema
from .Timezone import *

def get_all():
    availabilitys = Availability.all()
    return availabilitys.all()

def add(availability_data: schema.AvailabilityBase):
    user =User.find(availability_data.user_id)
    if not user:
        return HTTPException(status_code=400, detail="Host not Found.")
    availability = Availability()
    for attr in vars(availability_data).keys():
        setattr(availability, attr,getattr(availability_data, attr))
    availability.save()
    return availability

def get(availability_id: int):
    availability = Availability.find(availability_id)
    if not availability:
        raise HTTPException(status_code=400, detail="Availability not Found")
    return availability

def availabilitys_by_user(user_id: int):
    availability = Availability.where("user_id", user_id).get().all()
    return availability