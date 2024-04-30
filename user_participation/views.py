from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import ParticipationSerializer
from hackathons_registration.serializer import SectionSerializer
from team.serializers import Memberserializer,Teamserializer

# Create your views here.
@api_view(['GET'])
def get_participation_by_hackathons(request,team_id,hackathon_id):
    team = Team.objects.get(_id=team_id)
    serializer = Teamserializer(team,many = False)
    return Response(serializer.data,status=status.HTTP_200_OK)
