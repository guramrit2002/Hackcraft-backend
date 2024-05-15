from rest_framework import serializers

class HackthonDashboardSerializer(serializers.Serializer):
    
    _id = serializers.CharField()
    logo = serializers.CharField()
    organisation = serializers.CharField()
    name = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    number_of_registerations = serializers.IntegerField()