from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer
from .models import Team,Members
from user_participation.serializers import ParticipationSerializer 
from user_participation.models import *
from user_participation.serializers import *
# from .models import AnonymousUser
class Memberserializer(ModelSerializer):
    
    class Meta:
        model = Members
        fields = '__all__'

class FieldSerializer(Serializer):
    
    def to_representation(self, data):
        app_id = data.get('application_id')
        
        long_fields = LongSerializer(Longfieldinput.objects.filter(registeration=app_id), many=True).data
        short_fields = ShortSerializer(Shortfieldinput.objects.filter(registeration=app_id), many=True).data
        multiple_fields = MultiplefieldSerializer(Multiplefieldinput.objects.filter(registeration=app_id), many=True).data
        toggle_fields = TogglefieldSerializer(Togglefieldinput.objects.filter(registeration=app_id), many=True).data
        stepper_fields = StepperSerializer(Stepperfieldinput.objects.filter(registeration=app_id), many=True).data
        date_fields = DatefieldSeriallizer(Datefieldinput.objects.filter(registeration=app_id), many=True).data
        slider_fields = SliderSerializer(Sliderfieldinput.objects.filter(registeration=app_id), many=True).data
        range_fields = RangeSerializer(RangefieldSlider.objects.filter(registeration=app_id), many=True).data
        linear_fields = LinearSerializer(LinearfieldSlider.objects.filter(registeration=app_id), many=True).data
        file_fields = FileuploadSerializer(Fileupload.objects.filter(registeration=app_id), many=True).data
        tag_fields = TagfieldSerializer(Tagfield.objects.filter(registeration=app_id), many=True).data
        response = []
        # Concatenate all the serialized data into a single list
        all_fields = long_fields + short_fields + multiple_fields + toggle_fields + \
                    stepper_fields + date_fields + slider_fields + range_fields + \
                    linear_fields + file_fields + tag_fields
                    
        field_map = {field['serial_number']: field for field in all_fields}
        print(field_map)
        response = [field_map.get(i, {}) for i in range(1, HackathonRegisterationForm.objects.get(_id = data.get('form')).number_of_fields + 1)]

        return {"fields": response}
class TeamGetserializer(ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

    def to_representation(self, instance):
        try:
            data_representation = super().to_representation(instance)
            team_id = data_representation.get('_id')
            members_qs = Members.objects.filter(team=team_id)
            members_count = members_qs.count()
            leader_present = members_qs.filter(is_leader=True).count() == 1

            if members_count <= data_representation.get('number_of_member'):
                if leader_present:
                    serializer = Memberserializer(members_qs, many=True)
                    serialized_members = serializer.data
                    result = {'team': data_representation, 'members': []}

                    for member_data in serialized_members:
                        member = Members.objects.get(_id=member_data.get('_id'))
                        participation_qs = Participation.objects.filter(member=member)
                        application_data = []
                        
                        for application in participation_qs:
                            fields_serializer = FieldSerializer({'application_id': application._id, 'form': application.form._id})
                            fields_data = fields_serializer.data['fields']
                            application_data.append({
                                'required_data':application,
                                'is_leader': member.is_leader,
                                'additional_data': fields_data
                            })
                        
                        result['members'].append({member.user.email: application_data or str(member.user._id)})
                    
                    return result
                else:
                    return {'error': "There must be exactly one leader in the team."}
            else:
                return {'error': "The number of members is full in this team."}
        except Exception as err:
            print(err)
            return {'error': str(err)}
        
        
class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'