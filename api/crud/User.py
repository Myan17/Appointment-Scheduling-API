from fastapi import HTTPException
from models.User import User
from models.Meeting import Meeting as Meetings
from crud.Meeting import *
import schema
from datetime import datetime
from .Timezone import *
def get_all():
    users = User.all()
    return users.all()

def add(user_data: schema.UserBase):
    user = User.where("email", user_data.email).get()
    if user:
        return HTTPException(status_code=400, detail="User already exists")
    user = User()
    for attr in vars(user_data).keys():
        setattr(user, attr,getattr(user_data, attr))
    user.timezone = getTimeZone(user_data.city + ", " + user_data.state)
    user.password = str(hash(user.password))
    user.save()
    return user

def get(user_id: int):
    user = User.find(user_id)
    if not user:
        raise HTTPException(status_code=400, detail="User not Found")
    return user

def get_by_email(email: str):
    user = User.where("email", email).get()
    if not user:
        raise HTTPException(status_code=400, detail="User not Found")
    return user

def getMeetingInfo(user_id: str):
    user = User.find(user_id)
    if not user:
        raise HTTPException(status_code=400, detail="User not Found")
    meetings = Meetings.where("organizer", user.email).get().all()
    data = {'name': user.name, 'email':user.email, 'gender': user.gender,'city': user.city, 'state': user.state, 'timezone': user.timezone}
    hosted_list = []
    for meeting in meetings:
        hosted_list.append(getMeetingWithParticipants(meeting.id))
    data ['hosted'] = hosted_list
    participated_list = []
    participated = Participant.where("participant_id", user.id).get().all()
    for part in participated:
        meeting = getMeetingWithParticipants(part.meeting_id)
        organizer = User.where("email", meeting.organizer).get().all()[0]
        time = getTime(meeting.date, meeting.time)
        newTime = convertTime(organizer.timezone, user.timezone, time)
        meeting.time = newTime.split(",")[1]
        meeting.date = newTime.split(",")[0]
        participated_list.append(meeting)
    data ['participated'] = participated_list
    return data