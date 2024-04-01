from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import response
# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from firebase_admin import auth
from .models import UserProfile,Skill
import json
from .serializers import Userprofileserializer,Userskill

@api_view(['GET'])
def userProfile(request,uid):
    print(uid)
    try:
        # Fetch the Firebase user by UID
        firebase_user = auth.get_user(uid)
        # Use the email to get the corresponding UserProfile
        profile_object = UserProfile.objects.get(email=firebase_user.email)
        
        # Serialize the UserProfile instance
        serializer = Userprofileserializer(profile_object)
        
        # Return the serialized data
        return Response(serializer.data)

    except UserProfile.DoesNotExist:
        return Response({"error": "UserProfile not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Log the exception and return a generic error message
        return Response({"error": "An error occurred while fetching user profile"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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