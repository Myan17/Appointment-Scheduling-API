from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from typing import List
import schema

from crud import User as Users
from crud import Leave as Leaves
from crud import Participant as Participants
from crud import Meeting as Meetings

app = FastAPI()

# Redirect root URL to documentation
@app.get("/")
async def docs_redirect():
    """
    Redirect to API documentation.
    
    Returns:
        RedirectResponse: Redirects to the /docs page.
    """
    response = RedirectResponse(url='/docs')
    return response

# User Routes
@app.get("/users/", response_model=List[schema.UserResult])
def get_all_users():
    """
    Fetch all users.

    Returns:
        List[schema.UserResult]: List of user objects.
    """
    return Users.get_all()

@app.post("/users/")
def add_user(user_data: schema.UserBase):
    """
    Add a new user.

    Args:
        user_data (schema.UserBase): Data for the new user.

    Returns:
        User: The newly created user object.
    """
    return Users.add(user_data)

@app.get("/users/{user_id}", response_model=schema.UserResult)
def get_single_user(user_id: int):
    """
    Fetch a single user by ID.

    Args:
        user_id (int): ID of the user.

    Returns:
        schema.UserResult: User object.

    Raises:
        HTTPException: If the user is not found.
    """
    user = Users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/{user_id}/meetings", response_model=schema.UserMeetings)
def get_meeting_info(user_id: int):
    """
    Fetch meeting information for a specific user.

    Args:
        user_id (int): ID of the user.

    Returns:
        schema.UserMeetings: User's meeting information.
    """
    return Users.getMeetingInfo(user_id)

# Leave Routes
@app.get("/unavailability/", response_model=List[schema.AvailabilityResult])
def get_all_unavailabilities():
    """
    Fetch all unavailability records.

    Returns:
        List[schema.AvailabilityResult]: List of unavailability records.
    """
    return Leaves.get_all()

@app.post("/unavailability/")
def add_unavailability(leave_data: schema.AvailabilityBase):
    """
    Add a new unavailability record.

    Args:
        leave_data (schema.AvailabilityBase): Data for the new record.

    Returns:
        AvailabilityResult: The created unavailability record.
    """
    return Leaves.add(leave_data)

@app.get("/unavailability/{leave_id}", response_model=schema.AvailabilityResult)
def get_single_unavailability(leave_id: int):
    """
    Fetch a single unavailability record by ID.

    Args:
        leave_id (int): ID of the unavailability record.

    Returns:
        schema.AvailabilityResult: The requested record.

    Raises:
        HTTPException: If the record is not found.
    """
    leave = Leaves.get(leave_id)
    if not leave:
        raise HTTPException(status_code=404, detail="Unavailability record not found")
    return leave

@app.get("/user/{user_id}/unavailability/", response_model=List[schema.AvailabilityResult])
def get_unavailability_by_user(user_id: int):
    """
    Fetch unavailability records for a specific user.

    Args:
        user_id (int): ID of the user.

    Returns:
        List[schema.AvailabilityResult]: List of unavailability records.
    """
    return Leaves.leaves_by_user(user_id)

# Participant Routes
@app.get("/participants/", response_model=List[schema.ParticipantResult])
def get_all_participants():
    """
    Fetch all participants.

    Returns:
        List[schema.ParticipantResult]: List of participants.
    """
    return Participants.get_all()

@app.get("/participants/{meeting_id}", response_model=List[schema.ParticipantResult])
def get_participants_by_meeting(meeting_id: int):
    """
    Fetch participants by meeting ID.

    Args:
        meeting_id (int): ID of the meeting.

    Returns:
        List[schema.ParticipantResult]: List of participants in the meeting.
    """
    return Participants.participants_by_meeting(meeting_id)

@app.get("/participants/{participant_id}/meetings", response_model=List[schema.MeetingResult])
def get_all_meetings(participant_id: int):
    """
    Fetch all meetings for a participant.

    Args:
        participant_id (int): ID of the participant.

    Returns:
        List[schema.MeetingResult]: List of meetings.
    """
    return Participants.get_meetings(participant_id)

@app.post("/participants/")
def add_participant(participant_data: schema.ParticipantBase):
    """
    Add a new participant.

    Args:
        participant_data (schema.ParticipantBase): Data for the new participant.

    Returns:
        ParticipantResult: The created participant object.
    """
    return Participants.add(participant_data)

# Meeting Routes
@app.get("/meetings/", response_model=List[schema.MeetingResult])
def get_all_meetings():
    """
    Fetch all meetings.

    Returns:
        List[schema.MeetingResult]: List of meetings.
    """
    return Meetings.get_all()

@app.post("/meetings/")
def add_meeting(meeting_data: schema.MeetingBase):
    """
    Add a new meeting.

    Args:
        meeting_data (schema.MeetingBase): Data for the new meeting.

    Returns:
        MeetingResult: The created meeting object.
    """
    return Meetings.add(meeting_data)

@app.get("/meetings/{meeting_id}", response_model=schema.Meetings)
def get_meeting_with_participants(meeting_id: int):
    """
    Fetch a meeting along with its participants.

    Args:
        meeting_id (int): ID of the meeting.

    Returns:
        schema.Meetings: The requested meeting object with participant details.

    Raises:
        HTTPException: If the meeting is not found.
    """
    meeting = Meetings.getMeetingWithParticipants(meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting
