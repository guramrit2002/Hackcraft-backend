from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField
from .models import *



class ParticipationSerializer(ModelSerializer):
    
    class Meta:
        model = Participation
        fields = '__all__'


class LongSerializer(ModelSerializer):
    
    field = SerializerMethodField()
    serial_number = SerializerMethodField()
    
    class Meta:
        model = Longfieldinput
        fields = ['_id', 'created', 'registeration', 'long_field','field','input','serial_number']
        
    def get_field(self, obj):
        if obj.long_field:
            return obj.long_field.label  # Assuming long_field is related to FieldModel
        return None
    
    def get_serial_number(self, obj):
        if obj.long_field:
            return obj.long_field.serial_number  # Assuming long_field is related to FieldModel
        return None

class ShortSerializer(ModelSerializer):
    
    field = SerializerMethodField()
    serial_number = SerializerMethodField()
    
    class Meta:
        model = Shortfieldinput
        fields = '__all__'
    
    def get_field(self, obj):
        if obj.short_field:
            return obj.short_field.label  # Assuming long_field is related to FieldModel
        return None
    
    def get_serial_number(self, obj):
        if obj.short_field:
            return obj.short_field.serial_number  # Assuming long_field is related to FieldModel
        return None

class DropdownfieldSerializer(ModelSerializer):
    
    field = SerializerMethodField()
    serial_number = SerializerMethodField()
    
    class Meta:
        model = Dropdownfieldinput
        fields = '__all__'
    
    def get_field(self, obj):
        if obj.dropdown_field:
            return obj.dropdown_field.label  # Assuming long_field is related to FieldModel
        return None
    
    def get_serial_number(self, obj):
        if obj.dropdown_field:
            return obj.dropdown_field.serial_number  # Assuming long_field is related to FieldModel
        return None

class MultiplefieldSerializer(ModelSerializer):
    
    field = SerializerMethodField()
    serial_number = SerializerMethodField()
    
    class Meta:
        model = Multiplefieldinput
        fields = '__all__'
        
    def get_field(self, obj):
        if obj.multiple_field:
            return obj.multiple_field.label  # Assuming long_field is related to FieldModel
        return None
    
    def get_serial_number(self, obj):
        if obj.multiple_field:
            return obj.multiple_field.serial_number  # Assuming long_field is related to FieldModel
        return None

class TogglefieldSerializer(ModelSerializer):
    
    field = SerializerMethodField()
    serial_number = SerializerMethodField()
    
    class Meta:
        model = Togglefieldinput
        fields = '__all__'
    
    def get_field(self, obj):
        if obj.toggle:
            return obj.toggle.label  # Assuming long_field is related to FieldModel
        return None
    
    def get_serial_number(self, obj):
        if obj.toggle:
            return obj.toggle.serial_number  # Assuming long_field is related to FieldModel
        return None
    
class StepperSerializer(ModelSerializer):
    
    field = SerializerMethodField()
    serial_number = SerializerMethodField()
    
    class Meta:
        model = Stepperfieldinput
        fields = '__all__'
    
    def get_field(self, obj):
        if obj.stepper_field:
            return obj.stepper_field.label  # Assuming long_field is related to FieldModel
        return None
    
    def get_serial_number(self, obj):
        if obj.stepper_field:
            return obj.stepper_field.serial_number  # Assuming long_field is related to FieldModel
        return None
        
class DatefieldSeriallizer(ModelSerializer):
    
    field = SerializerMethodField()
    serial_number = SerializerMethodField()
    
    class Meta:
        model = Datefieldinput
        fields = '__all__'
        
    def get_field(self, obj):
        if obj.date_field:
            return obj.date_field.label  # Assuming long_field is related to FieldModel
        return None
    
    def get_serial_number(self, obj):
        if obj.date_field:
            return obj.date_field.serial_number  # Assuming long_field is related to FieldModel
        return None
        

class SliderSerializer(ModelSerializer):
    
    field = SerializerMethodField()
    serial_number = SerializerMethodField()
    
    class Meta:
        model = Sliderfieldinput
        fields = '__all__'
    
    def get_field(self, obj):
        if obj.slider:
            return obj.slider.label  # Assuming long_field is related to FieldModel
        return None
    
    def get_serial_number(self, obj):
        if obj.slider:
            return obj.slider.serial_number  # Assuming long_field is related to FieldModel
        return None
        
    
class RangeSerializer(ModelSerializer):
    
    field = SerializerMethodField()
    serial_number = SerializerMethodField()
    
    class Meta:
        model = RangefieldSlider
        fields = '__all__'
    
    def get_field(self, obj):
        if obj.slider:
            return obj.slider.label  # Assuming long_field is related to FieldModel
        return None
    
    def get_serial_number(self, obj):
        if obj.slider:
            return obj.slider.serial_number  # Assuming long_field is related to FieldModel
        return None
        
    
class LinearSerializer(ModelSerializer):
    
    field = SerializerMethodField()
    serial_number = SerializerMethodField()
    
    class Meta:
        model = LinearfieldSlider
        fields = '__all__'
    
    def get_field(self, obj):
        if obj.slider:
            return obj.slider.label  # Assuming long_field is related to FieldModel
        return None
    
    def get_serial_number(self, obj):
        if obj.slider:
            return obj.slider.serial_number  # Assuming long_field is related to FieldModel
        return None
    
class FileuploadSerializer(ModelSerializer):
    
    field = SerializerMethodField()
    serial_number = SerializerMethodField()
    
    class Meta:
        model = Fileupload
        fields = '__all__'
    
    def get_field(self, obj):
        if obj.file_field:
            return obj.file_field.label  # Assuming long_field is related to FieldModel
        return None
    
    def get_serial_number(self, obj):
        if obj.file_field:
            return obj.file_field.serial_number  # Assuming long_field is related to FieldModel
        return None
        
class TagfieldSerializer(ModelSerializer):
    
    field = SerializerMethodField()
    serial_number = SerializerMethodField()
    
    class Meta:
        model = Tagfield
        fields = '__all__'
    
    def get_field(self, obj):
        if obj.tags_field:
            return obj.tags_field.label  # Assuming long_field is related to FieldModel
        return None
    
    def get_serial_number(self, obj):
        if obj.tags_field:
            return obj.tags_field.serial_number  # Assuming long_field is related to FieldModel
        return None
        