from django.shortcuts import render
from .serializer import *
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import uuid
from django.shortcuts import get_object_or_404
from hackathon_template.serializers import HackathonSerializer


@api_view(['GET'])
def hackathonGet(request):
    try:
        data = Hackathon.objects.all()
        serializer = HackathonSerializer(data, many=True)
        print(serializer.data)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def hackathon_regiteration_form_get(request):
    try:
        data = HackathonRegisterationForm.objects.all()
        serializer_regiter_form = HackathonRegistrationFormSerializer(data, many=True)
        return Response({"data": serializer_regiter_form.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def hackathon_registration_form_get_specific(request, id):
    try:
        # hakathon registerations form fetching using hackathon id
        form = get_object_or_404(HackathonRegisterationForm, hackathon___id=id)
        formserializer = HackathonRegistrationFormSerializer(form)
        # Initialize a array to collect all serialized data
        serialized_data = []

        # from here fields start fetching and serializing
        
        # Serialize LongAnswerField
        longfields = LongAnswerField.objects.filter(form=form)
        if longfields:
            data = LongAnswerFieldSerializer(longfields, many=True).data
            for i in data:
                i['type'] = 'long answer' 
            for i in data:
                serialized_data.append(i)
            
        # Serialize ShortAnswerField
        shortfields = ShortAnswerField.objects.filter(form=form)
        if shortfields:
            data= ShortAnswerFieldSerializer(shortfields, many=True).data
            for i in data:
                i['type'] = 'short answer'
            for i in data:
                serialized_data.append(i)
        
        # Serialize Radio Field
        radiofields = MultipleChoiceField.objects.filter(form=form, type='radio')
        if serialized_data:
            data = MultipleChoiceFieldSerializer(radiofields, many=True).data
            
            for i in data:
                i['type'] = 'radio'
                i['options'] = OptionSerializer(Options.objects.filter(field = i['_id'], related='RADIO'),many = True).data
            for i in data:
                print(i)
                serialized_data.append(i)
        
        # Serialize Check Field 
        checkfields = MultipleChoiceField.objects.filter(form=form, type='checkbox')
        if checkfields:
            data = MultipleChoiceFieldSerializer(checkfields, many=True).data
            for i in data:
                i['type'] = 'check'
                i['options'] = OptionSerializer(Options.objects.filter(field = i['_id'], related='CHECK'),many = True).data
            for i in data:
                print(i)
                serialized_data.append(i)

        # Serialize toggle Field
        togglefields = Toggle.objects.filter(form=form)
        if togglefields:
            data = ToggleSerializer(togglefields, many=True).data
            for i in data:
                i['type'] = 'toggle'
            for i in data:
                serialized_data.append(i)


        #Serialize Stepper Field 
        stepperfields = Stepper.objects.filter(form=form)
        if stepperfields:
            data = StepperSerializer(stepperfields, many=True).data
            for i in data:
                i['type'] = 'stepper'
            for i in data:
                serialized_data.append(i)


        # Serialize Date Field
        datefields = Date.objects.filter(form=form)
        if datefields:
            data = DateSerializer(datefields, many=True).data
            for i in data:
                i['type'] = 'date'
            for i in data:
                serialized_data.append(i)


        # Serialize Slider Field
        sliderfields = Slider.objects.filter(form=form, type='norange')
        if sliderfields:
            data = SliderSerializer(sliderfields, many=True).data
            for i in data:
                i['type'] = 'slider'
            for i in data:
                serialized_data.append(i)


        # Serialize range slider Field
        rangesliderfields = Slider.objects.filter(form=form, type='range')
        if rangesliderfields:
            data = SliderSerializer(rangesliderfields, many=True).data
            for i in data:
                i['type'] = 'range'
            for i in data:
                serialized_data.append(i)


        # Serialize linear slider field
        linearsliderfields = Slider.objects.filter(form=form, type='linear')
        if linearsliderfields:
            data = SliderSerializer(linearsliderfields, many=True).data
            for i in data:
                i['type'] = 'linear'
            for i in data:
                serialized_data.append(i)


        # Serialize File Upload Field
        fileuploadfields = Fileupload.objects.filter(form=form)
        if fileuploadfields:
            data = FileuploadSerializer(fileuploadfields, many=True).data
            for i in data:
                i['type'] = 'file'
            for i in data:
                serialized_data.append(i)


        # Serialized Tag Field
        tagsfields = Tags.objects.filter(form=form)
        if tagsfields:
            data = TagsSerializer(tagsfields, many=True).data
            for i in data :
                i['type'] = 'tag'
            for i in data:
                serialized_data.append(i)

            
        sorted_fields = []
        
        data = serialized_data
        # print(data)
        for i in range(1,form.number_of_fields):
            for j in data:
                if j['serial_number'] == i :
                    sorted_fields.append(j)                    
        
        #from here sections will be fetched and serialized 
        sections = Section.objects.filter(form = form)
        sectionserializer = SectionSerializer(sections,many = True)
        
        
        final_res = {
            'form':formserializer.data,
            'fields':sorted_fields,
            'sections': sectionserializer.data
        }
        
        return Response(final_res, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def hackathon_registeration_form_post(request,id):
    try:
        print(request.data)
        form = None
        body = request.data
        form_input = body['form']
        fields__input = body['fields']
        sections = body['sections']
        
        # creating new form with the hackathon id 
        form_input['hackathon'] = str(id)
        print(form_input)
        try:
            # print('form key is ready for serialization')
            form_serializer = HackathonRegistrationFormSerializer(data = form_input)
            if form_serializer.is_valid():
                # print('valid')
                form = form_serializer.save()
                
                # using type in fields for detecting type of field and serializing different fields
                for i in fields__input:
                    if i['type'] == 'long answer':
                        i['form'] = form._id
                        longserializer = LongAnswerFieldSerializer(data=i)
                        if longserializer.is_valid():
                            longserializer.save()
                    elif i['type'] == 'short answer':
                        print('short ', i['label'])
                        i['form'] = form._id
                        shortserializer = ShortAnswerFieldSerializer(data=i)
                        if shortserializer.is_valid():
                            shortserializer.save()
                    elif i['type'] == 'radio':
                        print('radio')
                        i['form'] = form._id
                        options= i['options']
                        del i['options'] 
                        multiplequestionserializer = MultipleChoiceFieldSerializer(data=i)
                        if multiplequestionserializer.is_valid():
                            field = multiplequestionserializer.save()
                            for option in options:
                                option['field'] = field._id 
                                optionserializer = OptionSerializer(data=option)
                                if optionserializer.is_valid():
                                    op = optionserializer.save()
                                    print(op.text)
                    elif i['type'] == 'check':
                        print('check')
                        i['form'] = form._id
                        options= i['options']
                        del i['options'] 
                        multiplequestionserializer = MultipleChoiceFieldSerializer(data=i)
                        if multiplequestionserializer.is_valid():
                            field = multiplequestionserializer.save()
                            for option in options:
                                option['field'] = field._id 
                                optionserializer = OptionSerializer(data=option)
                                if optionserializer.is_valid():
                                    op = optionserializer.save()
                                    print(op.text)
                    elif i['type'] == 'toggle':
                        print('toggle')
                        i['form'] = form._id
                        toggleserializer = ToggleSerializer(data=i)
                        if toggleserializer.is_valid():
                            toggleserializer.save()
                    elif i['type'] == 'stepper':
                        print('stepper')
                        i['form'] = form._id
                        stepperserializer = StepperSerializer(data=i)
                        if stepperserializer.is_valid():
                            stepperserializer.save()
                    elif i['type'] == 'slider':
                        print('slider')
                        i['form'] = form._id
                        sliderserializer = SliderSerializer(data=i)
                        if sliderserializer.is_valid():
                            sliderserializer.save()
                    elif i['type'] == 'range':
                        print('range')
                        i['form'] = form._id
                        sliderserializer = SliderSerializer(data=i)
                        if sliderserializer.is_valid():
                            sliderserializer.save()
                    elif i['type'] == 'linear':
                        print('linear')
                        sliderserializer = SliderSerializer(data=i)
                        if sliderserializer.is_valid():
                            sliderserializer.save()
                        i['form'] = form._id
                    elif i['type'] == 'file':
                        print('file')
                        i['form'] = form._id
                        sliderserializer = SliderSerializer(data=i)
                        if sliderserializer.is_valid():
                            sliderserializer.save()
                    elif i['type'] == 'tag':
                        i['form'] = form._id
                        print('tag')
                        sliderserializer = SliderSerializer(data=i)
                        if sliderserializer.is_valid():
                            sliderserializer.save()
                print(form._id)
                for i in sections:
                    i['form'] = form._id
                    section_serializer = SectionSerializer(data=i,many = False)
                    if section_serializer.is_valid():
                        section_serializer.save()
                else:
                    print(section_serializer.errors)
                return Response({
                    "message":"form is created",
                    "form_id":form_serializer.data['_id']
                    })
            else:
                return Response('something is not working in validation',status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            print(e)
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)