from django.db import models
from user.models import UserProfile
import uuid
from hackathon.models import Hackathons

# Create your models here.

class Team(models.Model):
    _id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    team_name = models.CharField(max_length=100)
    hackathon = models.ForeignKey(Hackathons,on_delete=models.CASCADE)
    number_of_member = models.IntegerField()
    

class Teamrequestedmembers(models.Model):
    _id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathons,on_delete=models.CASCADE,default=None)
    email = models.EmailField()
    
    def __str__(self) -> str:
        return str(self.team)+" "+str(self.email)
class Members(models.Model):
    _id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    team = models.ForeignKey(Team,on_delete = models.CASCADE)
    is_leader = models.BooleanField()
    
    def __str__(self):
        return str(self._id)
