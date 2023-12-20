from rest_framework import serializers
from .models import *


class HackathonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hackathon
        fields = '__all__'
    
    # def get_hackathon(self,obj):
    #     return {
    #         '_id': obj._id,
    #         'name': obj.name,
    #         'organisation_name': obj.organisation_name,
    #         'price': obj.fee,
    #         'start_date_time': obj.start_date_time,
    #         'team_size': obj.team_size,
    #         'mode_of_conduct': obj.mode_of_conduct,
    #         'venue': obj.venue,
    #         'Logo': obj.logo,
    #         'Image': obj.image1,  # You might need to adjust this based on your requirements
    #     }

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
        
        
