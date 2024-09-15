from fastapi import HTTPException
from models.Participant import Participant
from models.User import User
from models.Meeting import Meeting as MeetingModel
from crud import Meeting
import schema
from .Timezone import *


def get_all():
    participants = Participant.all()
    return participants.all()

def add(participant_data: schema.ParticipantBase):
    user =User.find(participant_data.participant_id)
    if not user:
        return HTTPException(status_code=400, detail="Participant not Found.")
    meeting = MeetingModel.find(participant_data.meeting_id)
    if not meeting:
        return HTTPException(status_code=400, detail="Meeting not Found.")
    participant = Participant()
    participant.participant_id = participant_data.participant_id
    participant.meeting_id = participant_data.meeting_id
    participant.save()
    return participant


def get_meetings(participant_id: int):
    participants = Participant.where("participant_id", participant_id).get().all()
    participant = User.find(participant_id)
    meetings = []
    for part in participants:
        meet = Meeting.get(part.meeting_id)
        user = User.where("email", meet.organizer).get().all()
        time = getTime(meet.date, meet.time)
        time = convertTime(user[0].timezone, participant.timezone, time)
        meet.time = time.split(",")[1]
        meet.date = time.split(",")[0]
        meetings.append(meet)
    return meetings

def participants_by_meeting(meeting_id: int):
    participants = Participant.where("meeting_id", meeting_id).get().all()
    return participants