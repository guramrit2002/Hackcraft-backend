from rest_framework.response import Response
from .models import *
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from hackathon.models import *
from itertools import chain
from default_template.models import Hackathon
# Create your views here.

@api_view(['GET'])
def gethackathon(request):
    try:
        hackathons = Hackathons.objects.filter(form_exist = True)
        print(hackathons)
        modified_data = []
        for hackathon in hackathons:
            defaults = Hackathon.objects.filter(hackathon = hackathon ) 
            for default in defaults:
                modified_data.append(
                    {
                        '_id': hackathon._id,
                        'name': hackathon.name,
                        'organisation_name': hackathon.organisation_name,
                        'price': hackathon.fee,
                        'start_date_time': hackathon.start_date_time,
                        'team_size': hackathon.team_size,
                        'mode_of_conduct': default.mode_of_conduct,
                        'venue': default.venue,
                        'Logo': hackathon.logo if hackathon.logo else '',
                        'Image': [default.image1,default.image2,default.image3,default.image4,default.image5],
                        'social':{
                            "discord":default.discord,
                            "facebook":default.facebook,
                            "email":default.email,
                            "twitter":default.twitter,
                            "linkedin":default.linkedin
                        }
                    }
                )
        
        
        
        return Response(modified_data,status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def defaultpage(request, id):
    try:
        hackathon = Hackathons.objects.get(_id = id)
        default = Hackathon.objects.get(hackathon = hackathon._id)
        round = Round.objects.filter(hackathon = default)
        try:
            hackathon_main_serializer = MainHackathonSerializer(hackathon,many = False)
        except Exception as e:
            print(e)
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        try:
            hackathon_serializer = HackathonSerializer(default, many=False)
            hackathon_data = hackathon_serializer.data
        except Exception as e:
            print('error : ',e)
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        
        
        images = []
        for i in range(5):
            if hackathon_data.get('image'+str(i+1))!="":
                hackathon_image = hackathon_data.get(hackathon_data['image'+str(i+1)])
                images.append(hackathon_image)
        
        del hackathon_data['image1']
        del hackathon_data['image2']
        del hackathon_data['image3']
        del hackathon_data['image4']
        del hackathon_data['image5'] 
        hackathon_data['images'] = images
        
        round_serializer = RoundSerializer(round,many=True)
        
        fields_data = []
        fields = Field.objects.filter(hackathon=default)
        for field in fields:
            field_serializer = FieldSerializer(field, many=False)
            text_properties = Textproperties.objects.get(field=field)
            property_serializer = FieldPropertiesSerializer(text_properties, many=False)
            field_data = field_serializer.data
            field_data['properties'] = property_serializer.data
            fields_data.append(field_data)
        
        containers_data = []
        containers = Container.objects.filter(hackathon=default)
        for container in containers:
            container_serializer = ContainerSerializer(container, many=False)
            container_property = Containerproperty.objects.get(container=container)
            property_serializer = ContainerPropertySerializer(container_property, many=False)
            container_data = container_serializer.data
            container_data['properties'] = property_serializer.data
            containers_data.append(container_data)
        
        # hackathon = 
        response_data = {
            'hackathon':hackathon_main_serializer.data,
            'default': hackathon_data,
            'round':round_serializer.data,
            'fields': fields_data,
            'containers': containers_data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    except Hackathon.DoesNotExist:
        return Response({'error': 'Hackathon not found'}, status=status.HTTP_404_NOT_FOUND)
    except Field.DoesNotExist:
        return Response({'error': 'Fields not found for the hackathon'}, status=status.HTTP_404_NOT_FOUND)
    except Container.DoesNotExist:
        return Response({'error': 'Containers not found for the hackathon'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def defaultpost(request):
    
    if request.method == 'POST':
        body = request.data
        if body :
            
            hackathon = body['hackathon']
            default = body['default']
            images = default['images']
            del default['images']
            
            for i in range(len(images)):
                print(images[i])
                default['image'+str(i+1)] = images[i] 
            
            user_email = hackathon['created_by']
            
            hackathon['created_by'] = UserProfile.objects.get(email = user_email)._id
            main_hackathon = MainHackathonSerializer(data= hackathon,many=False)
            if main_hackathon.is_valid():
                hack = main_hackathon.save()
                default['hackathon'] = hack._id
                hackathon_serializer = HackathonSerializer(data= default,many= False)
            
                if hackathon_serializer.is_valid():
                    new_default = hackathon_serializer.save()
                
                    for i in body.get('round', []):
                        
                        i['hackathon'] = str(new_default._id)
                        
                        round_serializer = RoundSerializer(data=i)
                        
                        if round_serializer.is_valid():
                            round_serializer.save()
                        else:
                            print(round_serializer.errors)
                            return Response({"error": round_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                    
                    for i in body['fields']:
                        field_serializer = FieldSerializer(data=i)
                        if field_serializer.is_valid():
                                field_serializer.validated_data['hackathon'] = new_default
                                field_serializer.validated_data['name'] = i['name']
                                field_serializer.validated_data['type'] = i['type']
                                new_field = field_serializer.save()
                                field_properties_serializer = FieldPropertiesSerializer(data = i['properties'])
                                if field_properties_serializer.is_valid():
                                    field_properties_serializer.validated_data['field'] = new_field
                                    field_properties_serializer.save()
                                else:
                                    print()
                                    return Response({"error":field_properties_serializer.errors},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        else:
                            print(field_serializer.errors)
                            return Response(field_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    for i in body['containers']:
                        container_serializer = ContainerSerializer(data=i)
                        if container_serializer.is_valid():
                            container_serializer.validated_data['hackathon'] = new_default
                            container_serializer.validated_data['name'] = i['name']
                            container_serializer.validated_data['type'] = i['type']
                            new_container = container_serializer.save()
                            container_property_serializer = ContainerPropertySerializer(data = i['properties'])
                            if container_property_serializer.is_valid():
                                container_property_serializer.validated_data['container'] = new_container
                                container_property_serializer.save()
                            else:
                                
                                return Response({"error":container_property_serializer.errors},status=status.HTTP_400_BAD_REQUEST)
                        else:
                            print(container_serializer.errors)
                            return Response({'error':container_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                        
                    return Response({'hackathon created':main_hackathon.data},status=status.HTTP_201_CREATED)
                else:
                    print(hackathon_serializer.errors)
                    return Response({"error":hackathon_serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            else:
                print(main_hackathon.errors)
                return Response({"error": main_hackathon.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:

            return Response({'error':'Response is required'},status=status.HTTP_400_BAD_REQUEST)
        