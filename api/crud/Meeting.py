from fastapi import HTTPException
from models.Meeting import Meeting as Meetings
from models.User import User
import schema
from .Timezone import *
from crud.Participant import participants_by_meeting

def get_all():
    """
    Fetch all meeting records.

    Returns:
        List[Meetings]: A list of all meeting records in the database.
    """
    meetings = Meetings.all()
    return meetings.all()

def add(meeting_data: schema.MeetingBase):
    """
    Add a new meeting record.

    Args:
        meeting_data (schema.MeetingBase): Data for the new meeting.

    Returns:
        Meetings: The created meeting record.

    Raises:
        HTTPException: If the meeting organizer is not found.
    """
    user = User.where("email", meeting_data.organizer).get()
    if not user:
        return HTTPException(status_code=400, detail="Host not Found.")
    meeting = Meetings()
    for attr in vars(meeting_data).keys():
        setattr(meeting, attr,getattr(meeting_data, attr))
    meeting.save()
    return meeting

def get(meeting_id: int):
    """
    Fetch a single meeting record by its ID.

    Args:
        meeting_id (int): The ID of the meeting.

    Returns:
        Meetings: The requested meeting record.

    Raises:
        HTTPException: If the meeting is not found.
    """
    meeting = Meetings.find(meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found.")
    return meeting

def getMeetingWithParticipants(meeting_id: int):
    """
    Fetch a meeting record along with its participants.

    Args:
        meeting_id (int): The ID of the meeting.

    Returns:
        schema.Meetings: A meeting object including participant details.

    Raises:
        HTTPException: If the meeting is not found.
    """
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

