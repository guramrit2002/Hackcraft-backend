from rest_framework.response import Response
from rest_framework.decorators import api_view
from user.models import UserProfile
from user_participation.models import Participation
from hackathon_template.models import HackathonViews,Hackathon,Round
from hackathons_registration.models import HackathonRegisterationForm
from rest_framework import status
from datetime import datetime
from .serializers import HackthonDashboardSerializer

@api_view(['GET'])
def dashboardgetapi(request,hackathon):
    participations = Participation.objects.filter(form = HackathonRegisterationForm.objects.get(hackathon = hackathon))
    number_of_participations= participations.count()
    impressions = HackathonViews.objects.filter( hackathon = hackathon).count()
    all_genders = {}
    genders = Participation.objects.filter(form = HackathonRegisterationForm.objects.get(hackathon = hackathon)).values("participant_gender")
    for gender in genders:
        if gender.get('participant_gender') in all_genders.keys():
            all_genders[gender.get('participant_gender')] += 1
        elif gender.get('participant_gender') not in all_genders.keys():
            all_genders[gender.get('participant_gender')] = 1
    hackathon_url = ''
    all_courses = {}
    for participation in participations:
        print('participation  :  ',participation.member.user.cousrse_name)
        if all_courses.get(participation.member.user.course_name) in all_courses.keys():
            if participation.member.user.cousrse_name != ' ':
                all_courses[participation.member.user.cousrse_name] += 1
            else :
                all_courses['Other branches'] += 1
        elif participation.member.user.cousrse_name not in all_courses.keys():
            if participation.member.user.cousrse_name != ' ':
                all_courses[participation.member.user.cousrse_name] = 1
            else :
                all_courses['Other branches'] = 1
                
    response = {
        "number_of_registerations" : number_of_participations,
        "number_of_impressions" : impressions,
        "gender_counts" : all_genders,
        "hackathon_url" : hackathon_url,
        "course_counts" : all_courses
    }
    return Response(response,status=status.HTTP_200_OK)

@api_view(['GET'])
def defaultgethackathons(request,email):
    try:
        hackathons = Hackathon.objects.filter(created_by = UserProfile.objects.get(email = email)._id)
        response = {
            'live':[],
            'open':[],
            'close':[]
        }
        print(hackathons)
        for hackathon in hackathons:
            print('hackathon id : ',hackathon._id)
            rounds = Round.objects.filter(hackathon = hackathon).values('start_timeline','end_timeline').order_by('serial_number')
            print('rounds : ',rounds)
            print(hackathon)
            if len(rounds):
                hackathon_objects = {
                        "_id" : hackathon._id,
                        "logo" : hackathon.logo,
                        "organisation" : hackathon.organisation_name,
                        "name":hackathon.name,
                        "start_date":hackathon.start_date_time.date(),
                        "end_date" : hackathon.deadline,
                        "number_of_registerations" : hackathon.number_of_registeration or 0
                    }
                start,end = rounds[0].get('start_timeline'),rounds[len(rounds)-1].get('end_timeline')
                print(start.date() <= datetime.now().date() and end.date() >= datetime.now().date())
                print(hackathon.deadline >= datetime.now().date())
                if hackathon.deadline < datetime.now().date():
                    
                    try:
                        serializer = HackthonDashboardSerializer(hackathon_objects)
                        response['close'].append(serializer.data)
                    except Exception as e:
                        print('error : ',e)
                        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
                    
                    if start.date() <= datetime.now().date() and end.date() >= datetime.now().date():
                        print('live',hackathon.name)
                        try:
                            serializer = HackthonDashboardSerializer(hackathon_objects)
                        except Exception as e:
                            print(e)
                            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
                        response['live'].append(serializer.data)
                
                elif hackathon.deadline >= datetime.now().date():
                    
                    print('open',hackathon.name)
                    try:
                        serializer = HackthonDashboardSerializer(hackathon_objects)
                    except Exception as e:
                        print(e)
                        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
                    response['open'].append(serializer.data)
                    if start.date() <= datetime.now().date() and end.date() >= datetime.now().date():
                        print('live',hackathon.name)
                        try:
                            serializer = HackthonDashboardSerializer(hackathon_objects)
                        except Exception as e:
                            print(e)
                            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
                        response['live'].append(serializer.data)
            
        return Response(response,status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)