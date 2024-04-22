from django.db import models
from user.models import UserProfile
import uuid
# Create your models here.

class Team(models.Model):
    _id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    team_name = models.CharField(max_length=100)
    number_of_member = models.IntegerField()
    

class Members(models.Model):
    _id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    team = models.ForeignKey(Team,on_delete = models.CASCADE)
    is_leader = models.BooleanField()