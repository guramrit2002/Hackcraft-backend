from django.db import models
from hackathon_template.models import Hackathon
import uuid

# Create your models here.


class HackathonRegisterationForm(models.Model):
    
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created = models.DateTimeField(auto_now_add=True)
    hackathon = models.ForeignKey(Hackathon,on_delete=models.CASCADE)
    participant_name = models.CharField(max_length=100,blank=True)
    participant_email = models.EmailField(max_length=254,blank=True)
    participant_phone = models.IntegerField(null=True)
    participant_gender = models.CharField(max_length=10,blank=True)
    
    def __str__(self):
        return str(self.hackathon)
    
class CustomField(models.Model):
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created = models.DateTimeField(auto_now_add=True)
    form = models.ForeignKey(HackathonRegisterationForm,on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{str(self.label)} | {str(self.form)}'
    
class ShortAnswerField(models.Model):
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created = models.DateTimeField(auto_now_add=True)
    custom_field = models.OneToOneField(CustomField, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    
    def __str__(self) -> str:
        return str(self._id)

class LongAnswerField(models.Model):
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created = models.DateTimeField(auto_now_add=True)
    custom_field = models.OneToOneField(CustomField, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    
    def __str__(self) -> str:
        return str(self._id)

class DropdownField(models.Model):
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created = models.DateTimeField(auto_now_add=True)
    custom_field = models.OneToOneField(CustomField, on_delete=models.CASCADE )
    choices = models.TextField()
    
    def getchoices(self):
        return[choice.strip() for choice in self.choices.split(',')]
    def __str__(self) -> str:
        return str(self._id)


class MultipleChoiceField(models.Model):
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created = models.DateTimeField(auto_now_add=True)
    custom_field = models.ForeignKey(CustomField, on_delete=models.CASCADE)
    option = models.CharField(max_length=500)
    
    def __str__(self) -> str:
        return str(self._id)
