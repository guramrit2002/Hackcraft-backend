from .models import AnonymousUser
from rest_framework.serializers import ModelSerializer

class AnonymousUserSerializer(ModelSerializer):
    
    class Meta :
        model = AnonymousUser
        fields = '__all__'
