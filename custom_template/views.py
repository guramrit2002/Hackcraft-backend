from django.shortcuts import render

# Create your views here.
from .models import *
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from rest_framework.response import Response
from hackathon.models import *
from default_template.serializers import MainHackathonSerializer
from .serializers import CustomTemplateSerializer

@api_view(['POST'])
def custompage(request):
    try:
        
        body = request.data
        print('body',body)
        hackathon = body['hackathon']
        hackathon['template'] = 'Custom'
        user_email = hackathon['created_by']
        user = UserProfile.objects.get(email = user_email)
        hackathon['created_by'] = user._id
        print('hackathon : ',hackathon)
        custom = body['custom']
        print('custom : ',custom)
        hackathon_serializer = MainHackathonSerializer(data = hackathon,many = False)
        if hackathon_serializer.is_valid():
            new_hackathon = hackathon_serializer.save()
            custom['hackathon'] = new_hackathon._id
            custom_serializer = CustomTemplateSerializer(data = custom,many = False)
            if custom_serializer.is_valid():
                custom_template = custom_serializer.save()
                return Response({"message":"new custom template is created","hackathon":new_hackathon._id,"custom_template":custom_template._id})
        else:
            print(hackathon_serializer.errors)
            return Response({'errors':hackathon_serializer.errors},status = status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response(str(e),status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def custompageget(request,hackathon):
    try:
        hackathon_associated = Hackathons.objects.get(
            _id = hackathon
        )
        custom_template = CustomTemplate.objects.get(
            hackathon = hackathon
        ) 
        hackathon_data = MainHackathonSerializer(hackathon_associated).data
        if hackathon_data['team_size_min'] and hackathon_data['team_size_max']:
            hackathon_data['team_size'] = [hackathon_data['team_size_min'],hackathon_data['team_size_max']]
            del hackathon_data['team_size_min']
            del hackathon_data['team_size_max']
        else:
            hackathon_data['team_size'] = [hackathon_data['team_size_min']]
            del hackathon_data['team_size_min']
            del hackathon_data['team_size_max']
        custom_template_date = CustomTemplateSerializer(custom_template).data
        
        return Response(
            {
                "hackathon":hackathon_data,
                "custom":custom_template_date
            }
        )
    except Exception as e:
        print(e)
        return Response(str(e),status = status.HTTP_400_BAD_REQUEST)