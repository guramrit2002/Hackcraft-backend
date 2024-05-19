from rest_framework import serializers
from .models import (HackathonRegisterationForm, ShortAnswerField, LongAnswerField,
                     DropdownField,OptionDropdown, MultipleChoiceField, Toggle, Stepper, Date,
                     Slider, File, Tags,Section,Options,TagOptions)

class HackathonRegistrationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = HackathonRegisterationForm
        fields = '__all__'

class ShortAnswerFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortAnswerField
        fields = '__all__'

class LongAnswerFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = LongAnswerField
        fields = '__all__'

class DropdownFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = DropdownField
        fields = '__all__'
class DropdownOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionDropdown
        fields=  '__all__'
class MultipleChoiceFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceField
        fields = '__all__'

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Options
        fields = '__all__'
class ToggleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Toggle
        fields = '__all__'

class StepperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stepper
        fields = '__all__'

class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = '__all__'

class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'

class FileuploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'

class TagOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagOptions
        fields = '__all__'
        
class SectionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Section
        fields = '__all__'
        
