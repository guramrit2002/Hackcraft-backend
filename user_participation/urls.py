from django.urls import path
from .views import get_participation_by_hackathons,post_participation
from .models import *

urlpatterns = [
    path('getall/<team_id>',get_participation_by_hackathons),
    path('post/<member_id>',post_participation),
    
]
