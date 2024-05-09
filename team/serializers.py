from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer
from .models import Team,Members
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
        all_fields = []
        if long_fields :
            all_fields+=long_fields
        elif short_fields : 
            all_fields += short_fields
        elif multiple_fields:
            all_fields+=multiple_fields
        elif toggle_fields:
            all_fields+=toggle_fields
        elif stepper_fields:
            all_fields+=stepper_fields
        elif date_fields:
            all_fields+=date_fields
        elif slider_fields:
            all_fields += slider_fields
        elif range_fields:
            all_fields+=range_fields
        elif linear_fields:
            all_fields+=linear_fields
        elif file_fields:
            all_fields+=file_fields
        elif tag_fields:
            all_fields+=tag_fields
        field_map = {field['serial_number']: field for field in all_fields}
        for i in range(1, len(field_map.keys())+1):
            print('i : ',i)
            print('serial_number',field_map.get(i))
            if field_map.get(i):
                print('field with serial number : ',field_map.get(i))
                response.append(field_map.get(i))
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
                        participation = Participation.objects.get(member=member_data.get('_id'))
                        
                        participation_serializer = ParticipationSerializer(participation,many=False)
                        participation_qs = participation_serializer.data
                        application_data=[]
                        fields_serializer = FieldSerializer({'application_id': participation_qs.get('_id'), 'form': participation_qs.get('form')})
                        fields_data = fields_serializer.data['fields']

                        application_data.append({
                                'required_data': participation_qs,
                                'is_leader': member_data.get('is_leader'),
                                'additional_data': fields_data
                            })
                        email = UserProfile.objects.get(_id = member_data.get('user')).email
                        result['members'].append({email: application_data or str(member_data.user._id)})
                    print('result',result)
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