from rest_framework.serializers import ModelSerializer
from .models import UserProfile,Skill

# start code from here 

class Userprofileserializer(ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = '__all__'

class Userskill(ModelSerializer):
    
    class Meta:
        model = Skill
        fields = '__all__'
