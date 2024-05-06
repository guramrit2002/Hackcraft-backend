from .models import Team,Members
from rest_framework.response import Response
# from .serializers import Teamserializer,Memberserializer
from rest_framework.decorators import api_view
from rest_framework import status
from user.models import UserProfile
from .serializers import TeamSerializer,Memberserializer
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

@api_view(['POST'])
def teampost(request):
    try:
        body = request.data
        team_data = body.get('team')
        leader = body.get('leader')
        try:
            team = Team.objects.get(team_name = team_data['team_name'])
            
            return Response({
                'message':'Team name is already taken'
            },status=status.HTTP_400_BAD_REQUEST)
            
        except Team.DoesNotExist:
            team_serializer = TeamSerializer(data = team_data,many = False)
            if team_serializer.is_valid():
                team_serializer.save()
                team_data = team_serializer.data
                team_id = team_data['_id']
                user_id = UserProfile.objects.get(email = leader['email'])._id
                leader['team'] = team_id
                leader['user'] = user_id
                leader['is_leader'] = True
                leader_serializer = Memberserializer(data=leader,many = False)
                if leader_serializer.is_valid():
                    leader_serializer.save()
                    return Response({
                        "message":"new team is created",
                        "team_id":team_id,
                        "leader":leader_serializer.data['_id']
                    })
                else:
                    return Response(leader_serializer.errors)
            else:
                return Response(team_serializer.errors)
        except Exception as e:
            print(e)
            return Response(str(e))
    except Exception as e:
        print(e)
        return Response(str(e))