from rest_framework import serializers
from .models import *


class HackathonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hackathon
        fields = '__all__'
    
    # def to_representation(self, data):
    #     print('data : ',data.images)
    #     images = data.images
    #     response = data.copy()  
    #     del response['images']
    #     for i in range(len(images)):
    #         response['images'+str(i+1)] = images[i] 
    #     return super().to_representation(response)
            

class RoundSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Round
        fields = '__all__'
        
    def to_representation(self, instance):
        return super().to_representation(instance)

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
        
        
