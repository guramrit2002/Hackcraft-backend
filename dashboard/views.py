from rest_framework.response import Response
from rest_framework.decorators import api_view
from user_participation.models import Participation
from hackathon_template.models import HackathonViews
from hackathons_registration.models import HackathonRegisterationForm
from rest_framework import status

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
        if all_courses.get(participation.member.user.cousrse_name) in all_courses.keys():
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