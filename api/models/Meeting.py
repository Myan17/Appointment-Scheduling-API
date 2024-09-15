""" Meeting Model """

from masoniteorm.models import Model
from masoniteorm.relationships import has_many

class Meeting(Model):
    """Meeting Model"""
    @has_many("id", "meeting_id")
    def invites(self):
        from .Invite import Invite
        return Invite
    
    @has_many("id", "meeting_id")
    def participants(self):
        from .Participant import Participant
        return Participant
    pass
