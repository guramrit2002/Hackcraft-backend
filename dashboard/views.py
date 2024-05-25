from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from user.models import UserProfile
from team.models import Team, Members
from user_participation.models import *
from default_template.models import HackathonViews,Hackathon,Round
from rest_framework import status
from datetime import datetime
from .serializers import HackthonDashboardSerializer
from itertools import chain


@api_view(['GET'])
def dashboardgetapi(request,hackathon):
    hackathon = Hackathon.objects.get(_id = hackathon)
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
        "course_counts" : all_courses,
        "social" : {"discord":hackathon.discord,"email":hackathon.email,"linkedin":hackathon.linkedin,"website":hackathon.website,"github":hackathon.github,"facebook":hackathon.facebook,"twitter":hackathon.twitter}
    }
    return Response(response,status=status.HTTP_200_OK)


def dashboardcustomemail(request):
    try:
        body = request.body
        
    except Exception as e:
        print(e)
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def defaultgethackathons(request,email):
    try:
        hackathons = Hackathons.objects.filter(created_by = UserProfile.objects.get(email = email)._id)
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
    
    
@api_view(['GET'])
def dashboardteamget(request,hackathon):
        
    try:
        q = request.query_params.get('q') or None
        teams = Team.objects.filter(hackathon = hackathon)
        form = HackathonRegisterationForm.objects.get(hackathon = hackathon)
        fields = [
                    LongAnswerField.objects.filter(form=form),
                    ShortAnswerField.objects.filter(form=form),
                    MultipleChoiceField.objects.filter(form=form),
                    DropdownField.objects.filter(form=form),
                    Toggle.objects.filter(form=form),
                    Stepper.objects.filter(form=form),
                    Date.objects.filter(form=form),
                    Slider.objects.filter(form=form,type = 'slider'),
                    Slider.objects.filter(form=form,type = 'linear'),
                    Slider.objects.filter(form=form, type = 'range'),
                    File.objects.filter(form=form),
                    Tags.objects.filter(form=form)
                ]
        
        all_form_fields = list(chain.from_iterable(fields))
        print('all_form_fields : ',Slider.objects.filter(form=form,type = 'slider').values('label'))
        
        all_fields = []
        for index in range(len(all_form_fields)):
            all_fields.append(all_form_fields[index].label)
        print('all fields in form : ',all_fields)
        response = []
        for team in teams:
            members = Members.objects.filter(team = team)
            leader = "" 
            reg_status = ""
            
            if team.number_of_member == len(members):
                reg_status = "Completed"
            
            elif team.number_of_member < len(members):
                reg_status = "Incompleted"
            
            team_obj = {
                    "team":{
                            "team_name" : team.team_name,
                            "team_member_count":team.number_of_member,
                            "team_count":team.number_of_member,
                            "registeration_status":reg_status,
                            "registeration_date":"",
                            "leader" : leader ,
                            "all_fields":all_fields
                        },
                    "members": []
            } 
            
            # print('team_obj : ',team_obj)
            # response = team_obj
            for member in members:
                if member.is_leader:
                    team_obj["team"]["leader"] = member.user.first_name + ' ' + member.user.last_name
                print(leader)
                
                participation = Participation.objects.get(member=member)
                queries = [
                    
                    Longfieldinput.objects.filter(registeration=participation),
                    Shortfieldinput.objects.filter(registeration=participation),
                    Multiplefieldinput.objects.filter(registeration=participation),
                    Dropdownfieldinput.objects.filter(registeration=participation),
                    Togglefieldinput.objects.filter(registeration=participation),
                    Stepperfieldinput.objects.filter(registeration=participation),
                    Datefieldinput.objects.filter(registeration=participation),
                    Sliderfieldinput.objects.filter(registeration=participation),
                    RangefieldSlider.objects.filter(registeration=participation),
                    LinearfieldSlider.objects.filter(registeration=participation),
                    Fileupload.objects.filter(registeration=participation),
                    Tagfield.objects.filter(registeration=participation)
                    
                ]
                
                all_fields = list(chain.from_iterable(queries))
                field_res = {}
                print(len(all_form_fields))
                # print(len(all_form_fields))
                for index in range(len(all_form_fields)):
                    print(index)
                    if hasattr(all_fields[index], 'long_field'):
                        print(all_form_fields[index])
                        field_res[all_form_fields[index].label] = all_fields[index].input
                        print(all_fields)
                    elif hasattr(all_fields[index], 'short_field'):
                        field_res[all_form_fields[index].label] = all_fields[index].input
                        print(all_fields)
                    elif hasattr(all_fields[index], 'multiple_field'):
                        field_res[all_form_fields[index].label]  = all_fields[index].input.get('option')
                        print(all_fields)
                    elif hasattr(all_fields[index], 'toggle') and all_fields[index].toggle:
                        print(all_fields)
                        field_res[all_form_fields[index].label] = all_fields[index].input
                    elif hasattr(all_fields[index], 'stepper_field') and all_fields[index].stepper_field:
                        print(all_fields)
                        field_res[all_form_fields[index].label] = all_fields[index].input
                    elif hasattr(all_fields[index], 'date_field') and all_fields[index].date_field:
                        print(all_fields)
                        field_res[all_form_fields[index].label] =  all_fields[index].input
                    elif hasattr(all_fields[index], 'slider') and all_fields[index].slider:
                        print(all_fields)
                        print('sliders')
                        field_res[all_form_fields[index].label] =  all_fields[index].input
                    elif hasattr(all_fields[index], 'file_field') and all_fields[index].file_field:
                        print(all_fields)
                        field_res[all_form_fields[index].label] =  all_fields[index].input
                    elif hasattr(all_fields[index], 'tags_field') and all_fields[index].tags_field:
                        print(all_fields)
                        field_res[all_form_fields[index].tags_field] =  all_fields[index].input
                
                print('all form: ',field_res)
                
                member_obj = {
                    "user_first_name":member.user.first_name,
                    "user_last_name":member.user.last_name,
                    "is_leader":member.is_leader,
                    "submited_details":field_res,
                    }
                team_obj['members'].append(member_obj)
                team_obj['team']["registeration_date"] = participation.created
            response.append(team_obj)
            print(team_obj)
        return Response(response,status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
