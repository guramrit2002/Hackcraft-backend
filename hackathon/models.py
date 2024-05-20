from django.db import models
from user.models import UserProfile
import uuid

class Hackathons(models.Model):
    
    _id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False, 
        unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='hackathon_user')
    logo = models.CharField(
        max_length=2000,
        default="",
        blank =True)
    name = models.CharField(max_length=250)
    organisation_name = models.CharField(
        max_length=250,
        default = None)
    brief = models.TextField(default=None)
    deadline = models.DateField(
        auto_now=False, 
        auto_now_add=False)
    start_date_time = models.DateTimeField(
        auto_now=False, 
        auto_now_add=False)
    team_size = models.IntegerField()
    fee = models.CharField(
        max_length = 100 ,
        default=None,
        blank = True)
    total_number_rounds = models.IntegerField(
        blank=True,
        null=True)
    form_exist  = models.BooleanField(default = False)
    number_of_registeration = models.IntegerField(
        blank=True,
        default= None,
        null=True)
    
    def __str__(self) -> str:
        return self.name