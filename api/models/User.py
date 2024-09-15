""" User Model """

from masoniteorm.models import Model
from masoniteorm.relationships import has_many

class User(Model):
    """User Model"""
    @has_many("id", "user_id")
    def availabilitys(self):
        from .Availability import Availability
        return Availability
    
    @has_many("id", "participant_id")
    def participants(self):
        from .Participant import Participant
        return Participant
    
    @has_many("email", "organizer")
    def meetings(self):
        from .Meeting import Meeting
        return Meeting
    pass
