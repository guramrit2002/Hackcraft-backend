from django.db import models
from hackathons_registration.models import *
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
# Create your models here.


VISIBLE_CHOICES = (
    ('Public', 'Public'),
    ('Private', 'Private')
)
ALIGN_CHOICES = (
    ('right', 'right'),
    ('left', 'left'),
    ('center', 'center'),
    ('justify', 'justify')
)
FIELD_CHOICE = (
    ('text', 'text'),
    ('container', 'container'),
)


class Hackathon(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    logo = models.ImageField(upload_to='logo', max_length=250,null=True,blank=True)
    name = models.CharField(max_length=250)
    organisation_name = models.CharField(max_length=250,default = None)
    mode_of_conduct = models.CharField(max_length=250)
    deadline = models.DateField(auto_now=False, auto_now_add=False)
    team_size = models.IntegerField()
    visible = models.CharField(max_length=10, choices=VISIBLE_CHOICES)
    start_date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    about = models.TextField()
    brief = models.TextField(default=None)
    image1 = models.CharField(max_length=250,null=True,blank=True)
    image2 = models.CharField(max_length=250,null=True,blank=True)
    image3 = models.CharField(max_length=250,null=True,blank=True)
    image4 = models.CharField(max_length=250,null=True,blank=True)
    image5 = models.CharField(max_length=250,null=True,blank=True)
    fee = models.CharField(max_length = 100 ,default=None,null = True,blank = True)
    venue = models.CharField(max_length=500, default=None,)
    contact1_name = models.CharField(max_length=250, default=None,null = True,blank = True)
    contact1_number = models.IntegerField(default=None)
    contact2_name = models.CharField(max_length=250, default=None,null = True,blank = True)
    contact2_number = models.IntegerField(default=None)
    form_exist  = models.BooleanField(default = False)
    number_of_registeration = models.IntegerField(null = True,blank=True,default= None)
    discord = models.CharField(max_length = 200,null = True,blank=True,default= None)
    email = models.EmailField(null = True,blank=True,default= None)
    website = models.CharField(max_length=100,null = True,blank = True,default= None)
    github = models.CharField(max_length = 200,null = True,blank = True,default= '')
    facebook = models.CharField(max_length = 200,null = True,blank = True,default= '')
    twitter = models.CharField(max_length = 200,null = True,blank = True,default= '')
    linkedin = models.CharField(max_length = 200,null = True,blank = True,default= '')
    
    def __str__(self) -> str:
        return str(self.name)

class ThemeHackathon(models.Model):
    '''
    tags of hackathon data
    '''
    _id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    theme = models.CharField(max_length = 200)
    
    def __str__(self) -> str:
        return self.theme
class Round(models.Model):
    _id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    serial_number = models.IntegerField()
    name = models.CharField(max_length=20)
    description = models.TextField()
    start_timeline = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_timeline = models.DateTimeField(auto_now=False, auto_now_add=False)
    
    def __str__(self) -> str:
        return str(self._id)

    
class Field(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    hackathon = models.ForeignKey(Hackathon,on_delete = models.CASCADE,null = True,blank = True)
    name = models.CharField(max_length=200,null=True,blank=True)
    type = models.CharField(choices = FIELD_CHOICE, max_length = 200,null=True,blank=True)
    
    def __str__(self) -> str:
        return str(self.name)


class Textproperties(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    field = models.OneToOneField(Field,on_delete = models.CASCADE,null=True,blank=True)
    font = models.CharField(max_length=200,null=True,blank=True)
    size = models.IntegerField(null=True,blank=True)
    text_color = models.CharField(max_length=200,null=True,blank=True)
    font_weight = models.IntegerField(validators=[
        MinValueValidator(
            limit_value=100, message='Value must be greater than or equal to {limit_value}.'),
        MaxValueValidator(
            limit_value=900, message='Value must be less than or equal to {limit_value}.')
    ],null=True,blank=True)
    italics = models.BooleanField(null=True,blank=True)
    underline = models.BooleanField(null=True,blank=True)
    strikethrogh = models.BooleanField(null=True,blank=True)
    upper_case = models.BooleanField(null=True,blank=True)
    align = models.CharField(choices=ALIGN_CHOICES, max_length=10)
    letter_spacing = models.IntegerField(null=True,blank=True)
    letter_spacing = models.IntegerField(null=True,blank=True)
    
    def __str__(self) -> str:
        return str(self._id)
    

class Container(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    hackathon = models.ForeignKey(Hackathon,on_delete = models.CASCADE,null = True,blank = True)
    name = models.CharField(max_length=200)
    type = models.CharField(choices = FIELD_CHOICE, max_length = 200)
    
    def __str__(self) -> str:
        return str(self.name)
    
class Containerproperty(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, )
    container = models.OneToOneField(Container, on_delete = models.CASCADE,null=True,blank=True)
    Color = models.CharField(max_length=200,null=True,blank=True)
    border_color = models.CharField(max_length=200,null = False,blank=False)
    border_radius= models.DecimalField(max_digits=2,decimal_places=2,null = True,blank=True)
    box_shadow_color = models.CharField(max_length=200,null=True,blank=True)
    blur_radius = models.DecimalField(max_digits = 2,decimal_places=2,null = True,blank=True)
    focused_border_color = models.CharField(max_length=200,null = True,blank=True)
    border_width = models.IntegerField(null = True,blank=True)
    height = models.IntegerField(null = True,blank=True)
    
    
    def __str__(self) -> str:
        return str(self._id)
