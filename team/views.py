from .models import Team,Members
from rest_framework.response import Response
# from .serializers import Teamserializer,Memberserializer
from rest_framework.decorators import api_view
from rest_framework import status
from user.models import UserProfile
# from user.models import *

# @api_view(['GET'])
# def teamsget(request):
#     try:
#         teams = Team.objects.all()
#         serializer = Teamserializer(teams,many = True)
#         data = [team_data for team_data in serializer.data if team_data is not None]
#         return Response(data,status=status.HTTP_200_OK)
#     except Exception as e:
#         print(e)
#         return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

