from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField
from .models import *

class ParticipationSerializer(ModelSerializer):
    
    class Meta:
        model = Participation
        fields = '__all__'


class LongSerializer(ModelSerializer):
    
    long_field_label = SerializerMethodField()
    serial_number = SerializerMethodField()
    
    class Meta:
        model = Longfieldinput
        fields = ['_id', 'created', 'registeration', 'long_field','long_field_label','text','serial_number']
        
    def get_long_field_label(self, obj):
        print("working")
        print(obj.long_field)
        if obj.long_field:
            return obj.long_field.label
        print('None')
        return None
    
    def get_serial_number(self,obj):
        
        if obj.long_field:
            return obj.long_field.serial_number

class ShortSerializer(ModelSerializer):
    
    short_field_label = SerializerMethodField()
    serial_number = SerializerMethodField()
    
    class Meta:
        model = Shortfieldinput
        fields = '__all__'
    
    def get_short_field_label(self, obj):
        print("working")
        print(obj.short_field)
        if obj.short_field:
            return obj.short_field.label
        print('None')
        return None
    
    def get_serial_number(self,obj):
        
        if obj.short_field:
            return obj.short_field.serial_number

class DropdownfieldSerializer(ModelSerializer):
    
    
    class Meta:
        model = Dropdownfieldinput
        fields = '__all__'

class MultiplefieldSerializer(ModelSerializer):
    
    multiple_field_label = SerializerMethodField()
    serial_number = SerializerMethodField()
    
    class Meta:
        model = Multiplefieldinput
        fields = '__all__'
        
    def get_multiple_field_label(self, obj):
        print("working")
        print(obj.multiple_field)
        if obj.multiple_field:
            return obj.multiple_field.label
        print('None')
        return None

    def get_serial_number(self,obj):
        
        if obj.multiple_field:
            return obj.multiple_field.serial_number
        

class TogglefieldSerializer(ModelSerializer):
    
    toggle_field_label = SerializerMethodField()
    serial_number = SerializerMethodField()
    
    class Meta:
        model = Togglefieldinput
        fields = '__all__'
    
    def get_toggle_field_label(self, obj):
        print("working")
        print(obj.toggle)
        if obj.toggle:
            return obj.toggle.label
        print('None')
        return None
    
    def get_serial_number(self,obj):
        
        if obj.toggle:
            return obj.toggle.serial_number
    
class StepperSerializer(ModelSerializer):
    
    stepper_field_label = SerializerMethodField()
    serial_number = SerializerMethodField()
    
    class Meta:
        model = Stepperfieldinput
        fields = '__all__'
    
    def get_stepper_field_label(self, obj):
        print("working")
        print(obj.stepper_field)
        if obj.stepper_field:
            return obj.stepper_field.label
        print('None')
        return None
    
    def get_serial_number(self,obj):
        
        if obj.stepper_field:
            return obj.stepper_field.serial_number
        
class DatefieldSeriallizer(ModelSerializer):
    
    date_field_label = SerializerMethodField()
    serial_number = SerializerMethodField()
    
    class Meta:
        model = Datefieldinput
        fields = '__all__'
        
    def get_date_field_label(self, obj):
        print("working")
        print(obj.date_field)
        if obj.date_field:
            return obj.date_field.label
        print('None')
        return None
    
    def get_serial_number(self,obj):
        
        if obj.date_field:
            return obj.date_field.serial_number

class SliderSerializer(ModelSerializer):
    
    slider_field_label = SerializerMethodField()
    serial_number = SerializerMethodField()
    
    class Meta:
        model = Sliderfieldinput
        fields = '__all__'
    
    def get_slider_field_label(self, obj):
        print("working")
        print(obj.slider)
        if obj.slider:
            return obj.slider.label
        print('None')
        return None
    
    def get_serial_number(self,obj):
        
        if obj.slider:
            return obj.slider.serial_number
    
class RangeSerializer(ModelSerializer):
    
    range_field_label = SerializerMethodField()
    serial_number = SerializerMethodField()
    
    class Meta:
        model = RangefieldSlider
        fields = '__all__'
    
    def get_range_field_label(self, obj):
        print("working")
        print(obj.slider)
        if obj.slider:
            return obj.slider.label
        print('None')
        return None
    
    def get_serial_number(self,obj):
        
        if obj.slider:
            return obj.slider.serial_number
    
class LinearSerializer(ModelSerializer):
    
    linear_field_label = SerializerMethodField()
    serial_number = SerializerMethodField()
    
    class Meta:
        model = LinearfieldSlider
        fields = '__all__'
    
    def get_linear_field_label(self, obj):
        print("working")
        print(obj.slider)
        if obj.slider:
            return obj.slider.label
        print('None')
        return None
    
    def get_serial_number(self,obj):
        
        if obj.slider:
            return obj.slider.serial_number
    
class FileuploadSerializer(ModelSerializer):
    
    file_field_label = SerializerMethodField()
    serial_number = SerializerMethodField()
    
    class Meta:
        model = Fileupload
        fields = '__all__'
    
    def get_file_field_label(self, obj):
        print("working")
        print(obj.file_field)
        if obj.file_field:
            return obj.file_field.label
        print('None')
        return None
    
    def get_serial_number(self,obj):
        
        if obj.file_field:
            return obj.file_field.serial_number

class TagfieldSerializer(ModelSerializer):
    
    tag_field_label = SerializerMethodField()
    serial_number = SerializerMethodField()
    
    class Meta:
        model = Tagfield
        fields = '__all__'
    
    def get_tag_field_label(self, obj):
        print("working")
        print(obj.tags_field)
        if obj.tags_field:
            return obj.tags_field.label
        print('None')
        return None
    
    def get_serial_number(self,obj):
        
        if obj.tags_field:
            return obj.tags_field.serial_number