from django.shortcuts import render
from .serializer import *
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import uuid


@api_view(['GET'])
def hackathonGet(request):
    try:
        data = Hackathon.objects.all()
        serializer = HackathonSerializer(data, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
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
def hackathon_regiteration_form_get_specific(request, id):
    try:
        data = HackathonRegisterationForm.objects.filter(hackathon=Hackathon.objects.get(_id = id))
        # print(data.id)
        custom_field = CustomField.objects.filter(form=data[0])
        serializer_regiter_form = HackathonRegistrationFormSerializer(data, many=True)
        serializer_custom_field = CustomFieldSerializer(custom_field, many=True)
        return Response({
            "form": serializer_regiter_form.data,
            "custom_fields": serializer_custom_field.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def hackathon_registeration_form_post(request,id):
    try:
        if request.method == 'POST':
            request_body = request.data
            try:
                hackathon = Hackathon.objects.get(_id = id)
                print(hackathon)
            except Exception as e:
                return Response({'error':'Hackathon not found'},status = status.HTTP_404_NOT_FOUND)
            
            request_body["form"]["hackathon"] = str(hackathon._id)
            
            serializer_register_form = HackathonRegistrationFormSerializer(data=request_body["form"], many=False)
            if serializer_register_form.is_valid():
                
                serializer_register_form.validated_data['hackathon'] = hackathon
                print(serializer_register_form.validated_data['hackathon'])
                new_form = serializer_register_form.save()
                print(new_form)
                for custom_field_data in request_body.get("custom_fields", []):
                    custom_field_data['form'] = str(new_form._id)
                    serializer_custom_fields = CustomFieldSerializer(data=custom_field_data)
                    
                    if serializer_custom_fields.is_valid():
                        new_custom_field = serializer_custom_fields.save()
                        if custom_field_data.get("short_answer"):
                            short_answer_data = custom_field_data["short_answer"]
                            short_answer_data["custom_field"] = str(new_custom_field)
                            serializer_custom_short = ShortAnswerFieldSerializer(data=short_answer_data)
                            if serializer_custom_short.is_valid():
                                serializer_custom_short.save()
                            else:
                                return Response({"error": serializer_custom_short.errors}, status=status.HTTP_400_BAD_REQUEST)
                        elif custom_field_data.get("long_answer"):
                            long_answer_data = custom_field_data["long_answer"]
                            long_answer_data["custom_field"] = str(new_custom_field)
                            serializer_custom_large = LongAnswerFieldSerializer(data=long_answer_data)
                            if serializer_custom_large.is_valid():
                                serializer_custom_large.save()
                            else:
                                return Response({"error": serializer_custom_large.errors}, status=status.HTTP_400_BAD_REQUEST)
                        elif custom_field_data.get("multiple_choice"):
                            for option in custom_field_data.get("multiple_choice"):
                                option["custom_field"] = str(new_custom_field)
                                serializer_custom_multiple = MultipleChoiceFieldSerializer(data=option, many=False)
                                if serializer_custom_multiple.is_valid():
                                    serializer_custom_multiple.save()
                                else:
                                    return Response({"error": serializer_custom_multiple.errors}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"error": serializer_custom_fields.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error':serializer_register_form.errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message':'Registeration form is created'},status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Response
# {
#     "form": {
#         "participant_name": "",
#         "participant_email": "",
#         "participant_phone": 0,
#         "participant_gender": "",
#     },
#     "custom_fields": [
#         {
#             "short_answer": null,
#             "long_answer": null,
#             "multiple_choice": [
#                 {
#                     "option": "qwerty"
#                 },
#                 {
#                     "option": "qwerty1"
#                 }
#             ],
#             "label": "mcq",
#             "type": "Multiple"
#         }
#     ]
# }



