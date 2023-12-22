from rest_framework.response import Response
from .models import *
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
# Create your views here.

@api_view(['GET'])
def gethackathon(request):
    try:
        hackathons = Hackathon.objects.all()
        modified_data = [
            {
                '_id': hackathon._id,
                'name': hackathon.name,
                'organisation_name': hackathon.organisation_name,
                'price': hackathon.fee,
                'start_date_time': hackathon.start_date_time,
                'team_size': hackathon.team_size,
                'mode_of_conduct': hackathon.mode_of_conduct,
                'venue': hackathon.venue,
                'Logo': hackathon.logo.url if hackathon.logo else None,
                'Image': hackathon.image1.url if hackathon.image1 else None,
            }
            for hackathon in hackathons
        ]
        return Response(modified_data,status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def defaultpage(request, id):
    try:
        hackathon = Hackathon.objects.get(_id=id)
        round = Round.objects.filter(hackathon = hackathon)
        hackathon_serializer = HackathonSerializer(hackathon, many=False)
        round_serializer = RoundSerializer(round,many=True)
        fields_data = []
        fields = Field.objects.filter(hackathon=hackathon)
        for field in fields:
            field_serializer = FieldSerializer(field, many=False)
            text_properties = Textproperties.objects.get(field=field)
            property_serializer = FieldPropertiesSerializer(text_properties, many=False)
            field_data = field_serializer.data
            field_data['properties'] = property_serializer.data
            fields_data.append(field_data)
        containers_data = []
        containers = Container.objects.filter(hackathon=hackathon)
        for container in containers:
            container_serializer = ContainerSerializer(container, many=False)
            container_property = Containerproperty.objects.get(container=container)
            property_serializer = ContainerPropertySerializer(container_property, many=False)
            container_data = container_serializer.data
            container_data['properties'] = property_serializer.data
            containers_data.append(container_data)
        response_data = {
            'hackathon': hackathon_serializer.data,
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
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def defaultpost(request):
    
    if request.method == 'POST':
        body = request.data
        if body :
            hackathon = body['hackathon']
            hackathon_serializer = HackathonSerializer(data= hackathon,many= False)
            if hackathon_serializer.is_valid():
                new_hackathon = hackathon_serializer.save()
                for i in body.get('rounds', []):
                        i['hackathon'] = str(new_hackathon._id)
                        round_serializer = RoundSerializer(data=i)
                        if round_serializer.is_valid():
                            round_serializer.save()
                        else:
                            return Response({"error": round_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                    
                for i in body['fields']:
                    field_serializer = FieldSerializer(data=i)
                    if field_serializer.is_valid():
                            field_serializer.validated_data['hackathon'] = new_hackathon
                            field_serializer.validated_data['name'] = i['name']
                            field_serializer.validated_data['type'] = i['type']
                            new_field = field_serializer.save()
                            field_properties_serializer = FieldPropertiesSerializer(data = i['properties'])
                            if field_properties_serializer.is_valid():
                                field_properties_serializer.validated_data['field'] = new_field
                                field_properties_serializer.save()
                            else:
                                return Response({"error":field_properties_serializer.errors},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        return Response(field_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                for i in body['containers']:
                    container_serializer = ContainerSerializer(data=i)
                    if container_serializer.is_valid():
                        container_serializer.validated_data['hackathon'] = new_hackathon
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
                        return Response({'error':container_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                
            else:
                return Response({"error": hackathon_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':'Response is required'},status=status.HTTP_400_BAD_REQUEST)
        
    return Response({'message':'New default template is created'},status=status.HTTP_201_CREATED)

