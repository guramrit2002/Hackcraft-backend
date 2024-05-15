from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from firebase_admin import auth
from .models import UserProfile,Skill,OTP
from .serializers import Userprofileserializer,Userskill
from django.core.mail import send_mail
from hackathon_template.models import Hackathon
from hackathon_template.serializers import HackathonSerializer
from user_participation.models import Participation
from team.models import Team,Members
from hackathon_template.models import Round
from datetime import datetime

@api_view(['GET'])
def userProfile(request,uid):
    print('working')
    try:
        # Fetch the Firebase user by UID
        firebase_user = auth.get_user(uid)
        
        # Use the email to get the corresponding UserProfile
        profile_object = UserProfile.objects.get(email=firebase_user.email)
        
        # Serialize the UserProfile instance
        serializer = Userprofileserializer(profile_object)
        
        # iterating over skills ids and returning there name
        res_obj = serializer.data
        skills = []
        for i in res_obj['skill']:
            print(i)
            skill = Skill.objects.get(_id = i)
            skills.append(skill.skill_name)
        print(skills)
        res_obj['skill'] = skills
        
        # Return the response object
        return Response(res_obj)

    except UserProfile.DoesNotExist:
        return Response({"error": "UserProfile not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Log the exception and return a generic error message
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])

def userprofilepost(request):
    try:
        # Fetching email from request body
        email = request.data.get('email')

        # Getting user with the email to get uid
        user = auth.get_user_by_email(email=email)
        if user:
            # Fetching skills from request body
            skill_ids = []
            for skill_name in request.data.get('skill', []):
                try:
                    # Check if skill already exists
                    skill = Skill.objects.get(skill_name=skill_name)
                    skill_ids.append(skill._id)
                except Skill.DoesNotExist:
                    # Skill does not exist, create it
                    skill = Skill.objects.create(skill_name=skill_name)
                    skill_ids.append(skill._id)

            # Creating user profile
            user_profile_data = request.data.copy()
            user_profile_data['skill'] = skill_ids
            serializer = Userprofileserializer(data=user_profile_data)
            
            if serializer.is_valid():
                serializer.save()
                return Response('User profile created', status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['PUT'])
def userprofileput(request, uid):
    try:
        # Fetch the Firebase user by UID
        firebase_user = auth.get_user(uid)
    except auth.AuthError:
        return Response({'error': 'Firebase user not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        # Use the email to get the corresponding UserProfile
        profile = UserProfile.objects.get(email=firebase_user.email)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

    # Retrieve or create Skill objects using the skill names provided in the request
    skill_names = request.data.get('skill', [])
    skills = []
    for skill_name in skill_names:
        skill, created = Skill.objects.get_or_create(skill_name=skill_name)
        skills.append(skill)

    # Update the profile with the new skills
    profile.skill.set(skills)  # This clears old skills and adds new ones, modify if appending is needed instead

    # Serialize and save profile data
    serializer = Userprofileserializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User profile updated'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def profilecompletepercentage(request,email):
    try:
        user = UserProfile.objects.get(email = email)
        serializer = Userprofileserializer(user,many=False)
        user_dictionary = serializer.data
        keys = serializer.data.keys()
        empty = []
        number_of_nonempty_fields = 0
        for key in keys:
            if user_dictionary[key]:
                number_of_nonempty_fields+=1
            else:
                empty.append(key)
        return Response({
            'empty fields':empty,
            'profile_complete_percentage':(number_of_nonempty_fields*100)//len(keys)
            },status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)        




@api_view(['GET'])
def isregistered(request,email):
    try:
        profile = UserProfile.objects.get(email = email)
        # data_arr = [profile.username,,,,]
        if profile.username and profile.gender and profile.city and profile.organisation and profile.user_type:
            return Response('all required fields are avalable',status=status.HTTP_200_OK)
        else:
            return Response('fields are required to be filled',status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
def otpsend(request,email):
    try :
        if not email:
            return Response('please give the email to send the otp to',status=status.HTTP_400_BAD_REQUEST)
        elif OTP.objects.filter(user_email=email).exists():
            otp = OTP.objects.filter(user_email=email)
            otp.delete()
        otp = OTP.generate_otp(email=email)
        send_mail(
            'verification code for email verification',
            otp['otp'],
            'hackCraft@123',
            [email],
            fail_silently=False,
        )
        return Response({"otp":otp["otp_id"]})
    except Exception as e:
        return Response(str(e))

@api_view(['POST'])
def otprecieve(request):
    try:
        if not request.data['otp_id']:
            return Response('please provide the id of the otp',status=status.HTTP_400_BAD_REQUEST)
        otp = OTP.objects.get(id = request.data['otp_id'])
        print(otp.validate_otp(request.data['otp']))
        if otp.validate_otp(request.data['otp']):
            otp.delete()
            return Response('email verified successfully',status=status.HTTP_200_OK)
        elif otp.is_expired():
            otp.delete()
            return Response('your token is expired',status=status.HTTP_404_NOT_FOUND)
        else:
            return Response('your code is not correct',status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['Get'])
def otpreset(request,email):
    try:
        
        if not email:
                return Response('please give the email to send the otp to',status=status.HTTP_400_BAD_REQUEST)
        try:
            otp_instance = OTP.objects.get(user_email = email)
            otp_instance.delete()
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        try:
            otp = OTP.generate_otp(email=email)
            send_mail(
                'verification code for email verification',
                otp['otp'],
                'hackCraft@123',
                [email],
                fail_silently=False,
            )
            return Response({"otp":otp["otp_id"]})
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def dashboard_registered_hackathon(request, user_email):
    print(user_email)
    open = request.query_params.get('open') or None
    close = request.query_params.get('close') or None
    live = request.query_params.get('live') or None
    oldest = request.query_params.get('oldest') or None
    latest = request.query_params.get('latest') or None
    all = request.query_params.get('all') or None
    members = Members.objects.filter(user=UserProfile.objects.get(email=user_email))
    
    
    hackathons = []
    try:
        for member in members:
            print(member)
            filter_hackathons = Participation.objects.filter(member=member)
            
            for filter_hackathon in filter_hackathons:
                rounds = Round.objects.filter(hackathon = filter_hackathon.form.hackathon).values('start_timeline','end_timeline').order_by('serial_number')
                print('rounds : ',rounds)
                if len(rounds):
                    start,end = rounds[0].get('start_timeline'),rounds[len(rounds)-1].get('end_timeline')
                    
                    hackathon_object = {
                        'hackathon_name': filter_hackathon.form.hackathon.name,
                        'hackathon_host_date': filter_hackathon.form.hackathon.created_at,
                        'registered_on': filter_hackathon.created,
                        'organisation': filter_hackathon.form.hackathon.organisation_name,
                        'team': member.team.team_name,
                        'hackathon_deadline': filter_hackathon.form.hackathon.deadline,
                        'start' : start,
                        'end' : end
                    }
                    hackathons.append(hackathon_object)
        
                    def filterutility(hackathons,live,close,open,start,end):
                        if live:
                            
                            live_hackathons = []
                            print(live_hackathons)
                            for hackathon in hackathons:
                                if hackathon['start'].date() <= datetime.now().date() and hackathon['end'].date() >= datetime.now().date():
                                    print('live')
                                    hackathon['tag'] = 'live'
                                    live_hackathons.append(hackathon)
                                    print('live hackathon : ',live_hackathons)
                            hackathons = live_hackathons
                        elif close:
                            close_hackathon = []
                            for hackathon in hackathons:
                                if hackathon['hackathon_deadline'] < datetime.now().date():
                                    hackathon['tag'] = 'close'
                                    close_hackathon.append(hackathon)
                            hackathons = close_hackathon
                        elif open:
                            open_hackathon = []
                            for hackathon in hackathons:
                                if hackathon['hackathon_deadline'] >= datetime.now().date():
                                    hackathon['tag'] = 'open'
                                    open_hackathon.append(hackathon)
                            hackathons = open_hackathon
                        elif all:
                            for hackathon in hackathons:
                                hackathon['tag'] = 'all_hackathons'
                        return hackathons
                    
                    
                    if oldest:
                        hackathons.sort(key=lambda x: x['hackathon_host_date'], reverse=True)
                        hackathons = filterutility(hackathons,live,close,open,start,end)
                    elif latest:
                        hackathons.sort(key=lambda x: x['hackathon_host_date'])
                        hackathons = filterutility(hackathons,live,close,open,start,end)
                    elif not oldest and not latest:
                        hackathons = filterutility(hackathons,live,close,open,start,end)
            
        return Response(hackathons,status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(str(e),status= status.HTTP_400_BAD_REQUEST)