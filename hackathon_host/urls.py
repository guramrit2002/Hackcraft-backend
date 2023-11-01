from django.urls import path,include
from rest_framework import routers
from .views import HackathonViewset


router = routers.DefaultRouter()
router.register('hackathon',HackathonViewset,basename='hackathon')

urlpatterns = [
    path('',include(router.urls))
]
