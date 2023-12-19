from rest_framework import serializers
from .models import *


class HackathonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hackathon
        fields = '__all__'

class RoundSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Round
        fields = '__all__'

class FieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = Field
        fields = '__all__'
        
class FieldPropertiesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Textproperties
        fields = '__all__'

class ContainerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Container
        fields = '__all__'
        
class ContainerPropertySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Containerproperty
        fields = '__all__'
        
        
