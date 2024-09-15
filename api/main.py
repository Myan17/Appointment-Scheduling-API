from fastapi import FastAPI
from typing import List
import schema
from fastapi.responses import RedirectResponse

app = FastAPI()
@app.get("/")
async def docs_redirect():
    response = RedirectResponse(url='/docs')
    return response




from crud import User as Users
# For Users
@app.get("/users/", response_model=List[schema.UserResult])
def get_all_users():
    return Users.get_all()
@app.post("/users/")
def add_user(user_data: schema.UserBase):
    return Users.add(user_data)
@app.get("/users/{user_id}", response_model = schema.UserResult)
def get_single_user(user_id: int):
    return  Users.get(user_id)
@app.get("/users/{user_id}/meetings", response_model = schema.UserMeetings)
def get_meeting_info(user_id: int):
    return  Users.getMeetingInfo(user_id)





from crud import Leave as Leaves
@app.get("/unavailablity/", response_model=List[schema.AvailabilityResult])
def get_all_unavailabilities():
    return Leaves.get_all()
@app.post("/unavailablity/")
def add_unavailability(leave_data: schema.AvailabilityBase):
    response = Leaves.add(leave_data)
    return response
@app.get("/unavailablity/{leave_id}", response_model = schema.AvailabilityResult)
def get_single_unavailability(leave_id: int):
    leave =  Leaves.get(leave_id)
    return leave
@app.get("/user/{user_id}/unavailablity/", response_model = List[schema.AvailabilityResult])
def get_unavailability_by_user(user_id: int):
    leave =  Leaves.leaves_by_user(user_id)
    return leave



from crud import Participant as Participants
@app.get("/participants/", response_model=List[schema.ParticipantResult])
def get_all_participants():
    return Participants.get_all()
@app.get("/participants/{meeting_id}", response_model=List[schema.ParticipantResult])
def get_participants_by_meeting(meeting_id: int):
    return Participants.participants_by_meeting(meeting_id)
@app.get("/participants/{participant_id}/meetings", response_model=List[schema.MeetingResult])
def get_all_meetings(participant_id: int):
    return Participants.get_meetings(participant_id)
@app.post("/participants/")
def add_participant(participant_data: schema.ParticipantBase):
    response = Participants.add(participant_data)
    return response




from crud import Meeting as Meetings
@app.get("/meetings/", response_model=List[schema.MeetingResult])
def get_all_meetings():
    return Meetings.get_all()
@app.post("/meetings/")
def add_meeting(meeting_data: schema.MeetingBase):
    response = Meetings.add(meeting_data)
    return response
@app.get("/meetings/{meeting_id}", response_model = schema.Meetings)
def get_meeting_with_participants(meeting_id: int):
    return  Meetings.getMeetingWithParticipants(meeting_id)