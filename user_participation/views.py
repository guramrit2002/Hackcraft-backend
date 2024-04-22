from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import *
from hackathons_registration.serializer import SectionSerializer

# Create your views here.
@api_view(['GET'])
def get_participation_by_hackathons(request,hackathon_id):
    
    try:
        serialized_data = []
        form = HackathonRegisterationForm.objects.get(hackathon = hackathon_id)
        Participations = Participation.objects.filter(form = form )
        serializer = ParticipationSerializer(Participations,many=True)
        serialized_participations = serializer.data

        for participation in serialized_participations:

            participation_id = participation["_id"]
            longfields = Longfieldinput.objects.filter(registeration=participation_id)
            print(longfields)
            if longfields.exists():
                longfield_serializer = LongSerializer(longfields, many=True)
                serialized_data += longfield_serializer.data

            # Serialize ShortAnswerField
            shortfields = Shortfieldinput.objects.filter(registeration=participation_id)
            if shortfields:
                data= ShortSerializer(shortfields, many=True).data
                serialized_data+=(data)

            # Serialize Radio Field
            radiofields = Multiplefieldinput.objects.filter(registeration=participation_id)
            if serialized_data:
                data = MultiplefieldSerializer(radiofields, many=True).data
                serialized_data+= data

            # Serialize toggle Field
            togglefields = Togglefieldinput.objects.filter(registeration=participation_id)
            if togglefields:
                data = TogglefieldSerializer(togglefields, many=True).data
                serialized_data+=data

            #Serialize Stepper Field 
            stepperfields = Stepperfieldinput.objects.filter(registeration=participation_id)
            if stepperfields:
                data = StepperSerializer(stepperfields, many=True).data
                serialized_data+=data

            # Serialize Date Field
            datefields = Datefieldinput.objects.filter(registeration=participation_id)
            if datefields:
                data = DatefieldSeriallizer(datefields, many=True).data
                serialized_data+=data

            # Serialize Slider Field
            sliderfields = Sliderfieldinput.objects.filter(registeration=participation_id)
            if sliderfields:
                data = SliderSerializer(sliderfields, many=True).data
                serialized_data+=data

            # Serialize range slider Field
            rangesliderfields = RangefieldSlider.objects.filter(registeration=participation_id)
            if rangesliderfields:
                data = RangeSerializer(rangesliderfields, many=True).data
                serialized_data+=data

            # Serialize linear slider field
            linearsliderfields = LinearfieldSlider.objects.filter(registeration=participation_id)
            if linearsliderfields:
                data = LinearSerializer(linearsliderfields, many=True).data
                serialized_data+=data

            # Serialize File Upload Field
            fileuploadfields = Fileupload.objects.filter(registeration=participation_id)
            if fileuploadfields:
                data = FileuploadSerializer(fileuploadfields, many=True).data
                serialized_data+=data

            # Serialized Tag Field
            tagsfields = Tagfield.objects.filter(registeration=participation_id)
            if tagsfields:
                data = TagfieldSerializer(tagsfields, many=True).data
                serialized_data+=data
            
            sorted_fields = []
            print('number',form.number_of_fields)
            
            for i in range(1, form.number_of_fields + 1):
            # Use a list comprehension to find all items with the matching serial number
                matching_fields = [field for field in serialized_data if field.get('serial_number') == i]

                if matching_fields:
                    sorted_fields.extend(matching_fields)
                else:
                    # If no matching fields are found, you might want to handle it differently
                    sorted_fields.append({"serial_number": i, "info": "No data found"})
            
            sorted_fields = []
            print('number',form.number_of_fields)
            
            for i in range(1, form.number_of_fields + 1):
            # Use a list comprehension to find all items with the matching serial number
                matching_fields = [field for field in serialized_data if field.get('serial_number') == i]

                if matching_fields:
                    sorted_fields.extend(matching_fields)
                else:
                    # If no matching fields are found, you might want to handle it differently
                    sorted_fields.append({"serial_number": i, "info": "No data found"})
            
            sections = Section.objects.filter(form = form)
            sectionserializer = SectionSerializer(sections,many = True)
                
            return Response({
                "user-bio": serialized_participations,
                "additional_data": sorted_fields,
                "sections" : sectionserializer.data
            },status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)