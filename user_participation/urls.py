from django.urls import path
from .views import get_participation_by_hackathons
from .models import *

urlpatterns = [
    path('getall/<team_id>/<hackathon_id>',get_participation_by_hackathons)
]
