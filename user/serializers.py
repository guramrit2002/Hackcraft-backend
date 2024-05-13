from rest_framework.serializers import ModelSerializer,Serializer
from .models import UserProfile,Skill

# start code from here 

class Userprofileserializer(ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        extra_kwargs = {
            'user_type': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'username': {'required': False},
            'gender': {'required': False},
            'city': {'required': False},
            'organisation': {'required': False},
            'cousrse_name': {'required': False},
            'course_end_year': {'required': False},
            'date_of_birth': {'required': False},
            'interest': {'required': False},
            'about': {'required': False},
            'education_qualification': {'required': False},
            'specialization': {'required': False},
            'percentage': {'required': False},
            'skill': {'required': False},
            'degree': {'required': False},
            'facebook': {'required': False},
            'x': {'required': False},
            'instagram': {'required': False},
            'linkedin': {'required': False},
            'github': {'required': False},
            'medium': {'required': False},
            'reddit': {'required': False},
            'slack': {'required': False},
            'dribble': {'required': False},
            'behance': {'required': False},
            'codepen': {'required': False},
            'figma': {'required': False},
            'phone': {'required': False},
        }
    

class Userskill(ModelSerializer):
    
    class Meta:
        model = Skill
        fields = '__all__'
