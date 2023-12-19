# serializers.py
from rest_framework import serializers
from .models import *

class ShortAnswerFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortAnswerField
        fields = '__all__'

class LongAnswerFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = LongAnswerField
        fields = '__all__'

class MultipleChoiceFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = MultipleChoiceField
        fields = '__all__'


class CustomFieldSerializer(serializers.ModelSerializer):
    short_answer = ShortAnswerFieldSerializer(source='shortanswerfield', read_only=True)
    long_answer = LongAnswerFieldSerializer(source='longanswerfield', read_only=True)
    multiple_choice = MultipleChoiceFieldSerializer(source='multiplechoicefield_set', many=True,read_only=True)

    class Meta:
        model = CustomField
        fields = '__all__'

class HackathonRegistrationFormSerializer(serializers.ModelSerializer):
    custom_fields = CustomFieldSerializer(many=True, read_only=True)

    class Meta:
        model = HackathonRegisterationForm
        fields = '__all__'

