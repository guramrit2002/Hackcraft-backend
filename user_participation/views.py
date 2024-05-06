from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import ParticipationSerializer
from hackathons_registration.serializer import SectionSerializer
from team.serializers import TeamGetserializer
from .serializers import *

# Create your views here.
@api_view(['GET'])
def get_participation_by_hackathons(request,team_id):
    team = Team.objects.get(_id=team_id)
    serializer = TeamGetserializer(team,many = False)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['POST'])
def post_participation(request,member_id):
    
    body = request.data
    required = body['required']
    additional = body['additional']
    try:
        participation = Participation.objects.get(form = required.get('form'),member = member_id)
        return Response(
            {
                "message":"this member is already registered in this hackathon"
            },
            status=status.HTTP_400_BAD_REQUEST0)
    except Participation.DoesNotExist :
        required['member'] = member_id
        participation_serializer = ParticipationSerializer(data=required)
        if participation_serializer.is_valid():
            participation_serializer.save()
            id = participation_serializer.data.get('_id')
            for field in additional:
                if field['type'] == 'longAnswer':
                    del field['type']
                    field['registeration'] = id
                    field_id = field['long_field'] 
                    long = LongAnswerField.objects.get(_id = field_id)
                    if long.required:
                        if not field['input']:
                            return Response(f'{long.label} is required')
                    longserializer = LongSerializer(data = field,many = False)
                    if longserializer.is_valid():
                        longserializer.save()
                    else:
                        return Response(longserializer.errors)
                elif field['type'] == 'shortAnswer':
                    del field['type']
                    field['registeration'] = id
                    field_id = field['short_field'] 
                    short = ShortAnswerField.objects.get(_id = field_id)
                    if short.required:
                        if not field['input']:
                            return Response(f'{short.label} is required')
                    short_serializer = ShortSerializer(data=field,many = False)
                    if short_serializer.is_valid():
                        short_serializer.save()
                    else:
                        return Response(short_serializer.errors)
                elif field['type'] == 'multiple':
                    del field['type']
                    field['registeration'] = id
                    field_id = field['multiple_field'] 
                    multiple = MultipleChoiceField.objects.get(_id = field_id)
                    if multiple.required:
                        if not field['input']:
                            return Response(f'{multiple.label} is required')
                    multiple_serializer = MultiplefieldSerializer(data = field,many = False)
                    if multiple_serializer.is_valid():
                        multiple_serializer.save()
                elif field['type'] == 'toggle':
                    del field['type']
                    field['registeration'] = id 
                    field_id = field['toggle'] 
                    toggle = Toggle.objects.get(_id = field_id)
                    if toggle.required:
                        if not field['input']:
                            return Response(f'{toggle.label} is required')
                    togglefieldSerializer = TogglefieldSerializer(data = field, many = False)
                    if togglefieldSerializer.is_valid():
                        togglefieldSerializer.save()
                elif field['type'] == 'stepper':
                    del field['type']
                    field['registeration'] = id
                    field_id = field['stepper_field'] 
                    stepper = Stepper.objects.get(_id = field_id)
                    if stepper.required:
                        if not field['input']:
                            return Response(f'{stepper.label} is required')
                    stepperSerializer = StepperSerializer(data=field,many = False)
                    if stepperSerializer.is_valid():
                        stepperSerializer.save()
                elif field['type'] == 'date':
                    del field['type']
                    field['registeration'] = id
                    field_id = field['date_field'] 
                    date = Date.objects.get(_id = field_id)
                    if date.required:
                        if not field['input']:
                            return Response(f'{date.label} is required')
                    datefieldSeriallizer = DatefieldSeriallizer(data=field,many = False)
                    if datefieldSeriallizer.is_valid():
                        datefieldSeriallizer.save()
                elif field['type'] == 'slider':
                    del field['type']
                    field['registeration'] = id
                    field_id = field['slider'] 
                    slider = Slider.objects.get(_id = field_id,type='slider')
                    if slider.required:
                        if not field['input']:
                            return Response(f'{slider.label} is required')
                    sliderSerializer = SliderSerializer(data=field,many = False)
                    if sliderSerializer.is_valid():
                        sliderSerializer.save()
                elif field['type'] == 'range':
                    del field['type']
                    field['registeration'] = id
                    field_id = field['slider'] 
                    range = Slider.objects.get(_id = field_id,type='range')
                    if range.required:
                        if not field['input']:
                            return Response(f'{range.label} is required')
                    rangeSerializer = RangeSerializer(data=field,many = False)
                    if rangeSerializer.is_valid():
                        rangeSerializer.save()
                elif field['type'] == 'linear':
                    del field['type']
                    field['registeration'] = id
                    field_id = field['slider'] 
                    linear = Slider.objects.get(_id = field_id,type='linear')
                    if linear.required:
                        if not field['input']:
                            return Response(f'{linear.label} is required')
                    linearSerializer = LinearSerializer(data=field,many = False)
                    if linearSerializer.is_valid():
                        linearSerializer.save()
                elif field['type'] == 'file':
                    del field['type']
                    field['registeration'] = id
                    field_id = field['file_field'] 
                    file = Fileupload.objects.get(_id = field_id)
                    if file.required:
                        if not field['input']:
                            return Response(f'{file.label} is required')
                    fileuploadSerializer = FileuploadSerializer(data = field,many = False)
                    if fileuploadSerializer.is_valid():
                        fileuploadSerializer.save()
                elif field['type'] == 'tag':
                    del field['type']
                    field['registeration'] = id
                    field_id = field['tags_field'] 
                    tags = Tags.objects.get(_id = field_id)
                    if file.required:
                        if not field['input']:
                            return Response(f'{tags.label} is required')
                    tagfieldSerializer = TagfieldSerializer(data=field,many = False)
                    if tagfieldSerializer.is_valid():
                        tagfieldSerializer.save()
            return Response(
                {
                    "message":"participation is recorded",
                    "participation_id": id
                }
            )
        else:
            print(participation_serializer.errors)
            return Response(participation_serializer.errors)
    except Exception as e:
        print(e)
        return Response(str(e))