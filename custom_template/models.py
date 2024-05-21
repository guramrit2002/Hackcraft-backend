from django.db import models
import uuid
from default_template.models import Hackathons
# Create your models here.

class CustomTemplate(models.Model):
    
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hackathon = models.ForeignKey(Hackathons,on_delete=models.CASCADE,blank = True)
    
    def __str__(self) -> str:
        return self.hackathon

class Container(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    custom_template = models.ForeignKey(CustomTemplate,on_delete=models.CASCADE,blank = True)
    
    def __str__(self) -> str:
        return 