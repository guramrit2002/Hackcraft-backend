from django.db import models
from user.models import CustomUser
# Create your models here.

mode = (
    ('Online','Online'),
    ('Offline','Offline'),
)
visible = (
    ('Public','Public'),
    ('Private','Private')
    )

class Hackathon(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    logo = models.ImageField(upload_to='logo',max_length=250)
    name = models.CharField(max_length=250)
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    mode_of_conduct = models.CharField(max_length=250, choices=mode)
    deadline = models.DateField(auto_now=False, auto_now_add=False)
    team_size = models.IntegerField()
    visible = models.CharField(max_length=10, choices=visible)
    start_date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    about = models.TextField()
    brief = models.TextField(default=None)
    image1 = models.ImageField(upload_to='image',max_length=250)
    image2 = models.ImageField(upload_to='image',max_length=250)
    image3 = models.ImageField(upload_to='image',max_length=250)
    image4 = models.ImageField(upload_to='image',max_length=250)
    image5 = models.ImageField(upload_to='image',max_length=250)
    website = models.CharField(max_length=30)
    fee = models.DecimalField(max_digits=5, decimal_places=2, default=None)
    venue = models.CharField(max_length=500,default=None)
    contact1_name = models.CharField(max_length=250, default=None)
    contact1_number = models.IntegerField(default=None)
    contact2_name = models.CharField(max_length=250,default=None)
    contact2_number = models.IntegerField(default=None)
    
class Round(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    hackathon = models.ForeignKey(Hackathon,on_delete=models.CASCADE)
    serial_number = models.IntegerField()
    name = models.CharField(max_length=20)
    description = models.TextField()
    start_timeline = models.DateTimeField(auto_now=False,auto_now_add=False)
    end_timeline = models.DateTimeField(auto_now=False,auto_now_add=False)
    
class FAQ(models.Model):
    hackathon = models.ForeignKey(Hackathon,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    