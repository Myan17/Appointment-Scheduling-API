from fastapi import HTTPException
from models.Meeting import Meeting as Meetings
from models.User import User
import schema
from .Timezone import *
from crud.Participant import *

def get_all():
    meetings = Meetings.all()
    return meetings.all()

def add(meeting_data: schema.MeetingBase):
    user = User.where("email", meeting_data.organizer).get()
    if not user:
        return HTTPException(status_code=400, detail="Host not Found.")
    meeting = Meetings()
    for attr in vars(meeting_data).keys():
        setattr(meeting, attr,getattr(meeting_data, attr))
    meeting.save()
    return meeting

def get(meeting_id: int):
    meeting = Meetings.find(meeting_id)
    if not meeting:
        raise HTTPException(status_code=400, detail="Meeting not Found")
    return meeting

def getMeetingWithParticipants(meeting_id: int):
    meeting = Meetings.find(meeting_id)
    if not meeting:
        raise HTTPException(status_code=400, detail="Meeting not Found")
    participants = participants_by_meeting(meeting_id)

    data = {'meeting_id': meeting_id, 'date': meeting.date, 'time': meeting.time, 'title': meeting.title, 'organizer': meeting.organizer}
    list = []
    for participant in participants:
        list.append(User.find(participant.participant_id))
    data['participants'] = list
    return schema.Meetings(**data)