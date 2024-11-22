from fastapi import HTTPException
from models.Participant import Participant
from models.User import User
from models.Meeting import Meeting as MeetingModel
from crud import Meeting
import schema
from .Timezone import *

def get_all():
    """
    Fetch all participant records.

    Returns:
        List[Participant]: A list of all participant records in the database.
    """
    participants = Participant.all()
    return participants.all()

def add(participant_data: schema.ParticipantBase):
    """
    Add a new participant to a meeting.

    Args:
        participant_data (schema.ParticipantBase): Data for the new participant.

    Returns:
        Participant: The created participant record.

    Raises:
        HTTPException: If the user or meeting is not found.
    """
    user = User.find(participant_data.participant_id)
    if not user:
        raise HTTPException(status_code=404, detail="Participant not found.")
    
    meeting = MeetingModel.find(participant_data.meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found.")
    
    participant = Participant()
    participant.participant_id = participant_data.participant_id
    participant.meeting_id = participant_data.meeting_id
    participant.save()
    return participant

def get_meetings(participant_id: int):
    """
    Fetch all meetings for a specific participant.

    Args:
        participant_id (int): The ID of the participant.

    Returns:
        List[MeetingModel]: A list of meetings the participant is involved in.

    Raises:
        HTTPException: If the participant is not found.
    """
    participant = User.find(participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found.")

    participants = Participant.where("participant_id", participant_id).get().all()
    meetings = []

    for part in participants:
        meet = Meeting.get(part.meeting_id)
        if not meet:
            raise HTTPException(status_code=404, detail=f"Meeting with ID {part.meeting_id} not found.")
        
        # Fetch organizer's timezone and convert meeting time
        organizer = User.where("email", meet.organizer).first()
        if not organizer:
            raise HTTPException(status_code=404, detail="Organizer not found.")
        
        meeting_time = getTime(meet.date, meet.time)
        converted_time = convertTime(organizer.timezone, participant.timezone, meeting_time)
        
        meet.time = converted_time.split(",")[1]
        meet.date = converted_time.split(",")[0]
        meetings.append(meet)

    return meetings

def participants_by_meeting(meeting_id: int):
    """
    Fetch all participants for a specific meeting.

    Args:
        meeting_id (int): The ID of the meeting.

    Returns:
        List[Participant]: A list of participants in the meeting.
    """
    participants = Participant.where("meeting_id", meeting_id).get().all()
    if not participants:
        raise HTTPException(status_code=404, detail="No participants found for the given meeting ID.")
    return participants
