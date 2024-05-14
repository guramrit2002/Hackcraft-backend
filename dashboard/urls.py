from django.urls import path
from .views import dashboardgetapi

urlpatterns = [
    path('stats/<hackathon>',dashboardgetapi)
]
