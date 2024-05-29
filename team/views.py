from .models import Team,Members
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from user.models import UserProfile
from .serializers import TeamSerializer,Memberserializer,TeamGetserializer,RequestedEmail
from .models import *

@api_view(['GET'])
def get_participation_by_hackathons(request,team_id):
    team = Team.objects.get(_id=team_id)
    print(team)
    serializer = TeamGetserializer(team,many = False)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['POST'])
def teampost(request):
    try:
        body = request.data
        team_data = body.get('team')
        leader = body.get('leader')
        emails = body.get('emails')
        try:
            team = Team.objects.get(team_name = team_data['team_name'])
            return Response({
                    'message':'Team name is already taken'
                },status=status.HTTP_400_BAD_REQUEST)
        except Team.DoesNotExist:
            team_serializer = TeamSerializer(data = team_data,many = False)
            if team_serializer.is_valid() and leader:
                print('is valid')
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
                    for email in emails:
                        requested_emails = {
                            "team":team_id,    
                            "email":email,
                            "hackathon":team_data['hackathon']
                        }
                        email_serializer = RequestedEmail(data = requested_emails,many = False)
                        if email_serializer.is_valid():
                            email_serializer.save()
                        else:
                            return Response({"error":email_serializer.errors})
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
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def memberpost(request):
    try:
        body = request.data
        user_email = body['user']
        user = UserProfile.objects.get(email = user_email)._id
        body['user'] = user
        body['is_leader'] = False
        member_serializer = Memberserializer(data=body,many = False)
        if member_serializer.is_valid():
            member_serializer.save()
            print(member_serializer.data)
            return Response(
                {
                    "message":"member is created",
                    "member_id": member_serializer.data['_id']
                },
                status=status.HTTP_200_OK)
        else:
            return Response(member_serializer.errors)
    except UserProfile.DoesNotExist:
        print('user does not exist')
        return Response('user does not exist',status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
    



@api_view(['GET'])
def usertype(request, email, hackathon):
    try:
        user_profile = UserProfile.objects.get(email=email)
    except UserProfile.DoesNotExist:
        user_profile = None
    try:
        if user_profile:
            print('user profile : ',user_profile)
            try:
                
                    member = Members.objects.get(user=user_profile,team__hackathon=hackathon)
                    print(member)
                    team_id = member.team._id
                    role = "leader" if member.is_leader else "member"
                    return Response({
                        "role": role,
                        "team": team_id,
                        "message": f"already a {role} of a team"
                    })
            except Members.DoesNotExist:
                pass
            except Exception as e:
                print(e)
                return Response({'error': str(e)}, status=400)
            members_requested = Teamrequestedmembers.objects.filter(hackathon=hackathon, email=email)
            # print(members_requested)
            if members_requested:
                is_user = bool(user_profile)
                team_id = members_requested[0].team._id
                return Response({
                    "role": "pendin",
                    "is_user": is_user,
                    "team": team_id,
                    "message": "user exists but not a member" if is_user else "user does not exist and is not a member"
                })
            else:
                return Response({
                    "role": "firstuser",
                    "team": "",
                    "message": "new leader"
                })
    except Exception as e:
        return Response({'error': str(e)}, status=400)
