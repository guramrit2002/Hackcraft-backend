from django.db import models
from hackathons_registration.models import *
from user.models import UserProfile
from team.models import Team,Members
import uuid
# # Create your models here.


class Participation(models.Model):
    _id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    member = models.ForeignKey(Members,on_delete = models.SET_NULL,null = True)
    form = models.ForeignKey(HackathonRegisterationForm,on_delete=models.CASCADE)
    # main data required
    participant_name = models.CharField(max_length=100, blank=True)
    participant_email = models.EmailField(max_length=254, blank=True)
    participant_phone = models.IntegerField(null=True)
    participant_gender = models.CharField(max_length=10, blank=True)

    
    def __str__(self):
        return self.participant_name
    

class Longfieldinput(models.Model):
    _id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    registeration = models.ForeignKey(
        Participation, 
        on_delete=models.CASCADE
    )
    long_field = models.ForeignKey(
        LongAnswerField, 
        on_delete=models.CASCADE
    )
    # text data of long type i.e of 1000 or less char where space is a char 
    input = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.long_field.label


class Shortfieldinput(models.Model):
    _id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    registeration = models.ForeignKey(
        Participation, 
        on_delete=models.CASCADE
    )
    short_field = models.ForeignKey(
        ShortAnswerField, 
        on_delete=models.CASCADE
    )
    # text data of long type i.e of 500 or less char where space is a char 
    input = models.CharField(
        max_length=500
    )

class Dropdownfieldinput(models.Model):
    _id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    registeration = models.ForeignKey(
        Participation, 
        on_delete=models.CASCADE
    )
    # options selected 
    input = models.JSONField(default={})
    
class Multiplefieldinput(models.Model):
    _id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False)
    created = models.DateTimeField(auto_now_add=True)
    registeration = models.ForeignKey(
        Participation, 
        on_delete=models.CASCADE)
    multiple_field = models.ForeignKey(
        MultipleChoiceField, 
        on_delete=models.CASCADE)
    # options selected by user as json objects
    input = models.JSONField(default={})


class Togglefieldinput(models.Model):

    _id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    created = models.DateTimeField(
        auto_now_add=True
        )
    registeration = models.ForeignKey(
        Participation, 
        on_delete=models.CASCADE
        )
    toggle = models.ForeignKey(
        Toggle, 
        on_delete=models.CASCADE
    )
    input = models.BooleanField()


class Stepperfieldinput(models.Model):

    _id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    created = models.DateTimeField(
        auto_now_add=True
        )
    registeration = models.ForeignKey(
        Participation, 
        on_delete=models.CASCADE
        )
    stepper_field = models.ForeignKey(
        Stepper,
        on_delete=models.CASCADE,
        null=True
    )
    input = models.IntegerField()

class Datefieldinput(models.Model):

    _id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    created = models.DateTimeField(
        auto_now_add=True
        )
    registeration = models.ForeignKey(
        Participation, 
        on_delete=models.CASCADE
        )
    date_field = models.ForeignKey(
        Date,
        on_delete=models.CASCADE
    )
    # date between the set minimum and maximum date 
    input = models.DateField()


class Sliderfieldinput(models.Model):

    _id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    created = models.DateTimeField(
        auto_now_add=True
        )
    registeration = models.ForeignKey(
        Participation, 
        on_delete=models.CASCADE
        )
    slider = models.ForeignKey(
        Slider,
        on_delete=models.CASCADE
    )
    input = models.IntegerField()


class RangefieldSlider(models.Model):

    _id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    created = models.DateTimeField(
        auto_now_add=True
        )
    registeration = models.ForeignKey(
        Participation, 
        on_delete=models.CASCADE
        )
    slider = models.ForeignKey(
        Slider,
        on_delete=models.CASCADE
    )
    input1 = models.IntegerField()
    input2 = models.IntegerField()


class LinearfieldSlider(models.Model):

    _id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    created = models.DateTimeField(
        auto_now_add=True
        )
    registeration = models.ForeignKey(
        Participation, 
        on_delete=models.CASCADE
        )
    slider = models.ForeignKey(
        Slider,
        on_delete=models.CASCADE
    )
    input = models.IntegerField()

class Fileupload(models.Model):
    
    _id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    created = models.DateTimeField(
        auto_now_add=True
        )
    registeration = models.ForeignKey(
        Participation, 
        on_delete=models.CASCADE
        )
    file_field = models.ForeignKey(
        Fileupload,
        on_delete=models.CASCADE,
        null=True
    )
    input = models.FileField(
        upload_to='file_register', 
        max_length=100
        )
    
class Tagfield(models.Model):
    
    _id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    created = models.DateTimeField(
        auto_now_add=True
        )
    registeration = models.ForeignKey(
        Participation, 
        on_delete=models.CASCADE
        )
    tags_field = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE
    )
    input = models.JSONField(default={})