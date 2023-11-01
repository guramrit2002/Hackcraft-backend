from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Hackathon, Round
from .serializers import HackathonSerializer
# Create your views here.


class HackathonViewset(viewsets.ModelViewSet):
    queryset = Hackathon.objects.all()
    serializer_class = HackathonSerializer

