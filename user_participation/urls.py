from django.urls import path
from .views import post_participation
from .models import *

urlpatterns = [
    
    path('post/<member_id>',post_participation),
    
]
