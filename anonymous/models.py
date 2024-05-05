from django.db import models
from team.models import *
# Create your models here.

class AnonymousUser(models.Model):
    
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created_on = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.email