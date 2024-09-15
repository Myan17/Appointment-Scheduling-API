from pydantic import BaseModel
from typing import Optional, List

class UserBase(BaseModel):
    first_name: str
    middle_name: str
    surname: str
    email: str
    password: str
    cellphone: str
    gender: str
    city: str
    state: str
    zipcode: str
    timezone: str

class UserResult(UserBase):
    id: int
    class Config:
        orm_mode = True

class ParticipantBase(BaseModel):
    participant_id : int
    meeting_id : int

class ParticipantResult(ParticipantBase):
    id : int
    class Config:
        orm_mode = True

class AvailabilityBase(BaseModel):
    start_date: str
    end_date: str
    reason: str
    user_id: int

class AvailabilityResult(AvailabilityBase):
    id: int
    class Config:
        orm_mode = True

class MeetingBase(BaseModel):
    title: str
    date: str
    time: str
    organizer: str
class MeetingResult(MeetingBase):
    id: int
    class Config:
        orm_mode = True
        
class Meetings(BaseModel):
    meeting_id: int
    title: str
    date: str
    time: str
    organizer: str
    participants: List[UserResult] = []

class UserMeetings(BaseModel):
    first_name: str
    email: str
    gender: str
    city: str
    state: str
    timezone: str
    hosted: List[Meetings] = []
    participated: List[Meetings] = []