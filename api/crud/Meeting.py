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
    organizer = User.where("email", meeting_data.organizer).get()
    if not organizer:
        raise HTTPException(status_code=400, detail="Organizer not found.")
    
    meeting = Meetings()
    for attr in vars(meeting_data).keys():
        setattr(meeting, attr, getattr(meeting_data, attr))
    
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
        raise HTTPException(status_code=404, detail="Meeting not found.")

    participants = participants_by_meeting(meeting_id)
    participant_details = []

    for participant in participants:
        user = User.find(participant.participant_id)
        if user:
            participant_details.append(user)

    # Create a structured data object
    meeting_data = {
        'meeting_id': meeting_id,
        'date': meeting.date,
        'time': meeting.time,
        'title': meeting.title,
        'organizer': meeting.organizer,
        'participants': participant_details
    }
    return schema.Meetings(**meeting_data)

