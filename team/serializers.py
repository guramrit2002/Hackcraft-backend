from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer
from .models import Team,Members
from user_participation.serializers import ParticipationSerializer 
from user_participation.models import *
from user_participation.serializers import *

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
        print(HackathonRegisterationForm.objects.get(_id = data.get('form')).number_of_fields)
        for i in range(1,HackathonRegisterationForm.objects.get(_id = data.get('form')).number_of_fields):
            pass
            for j in all_fields:
                print()
                if i == j['serial_number']:
                    response.append(j)
        print(len(response))
        return {"fields": response}
class Teamserializer(ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

    def to_representation(self, data):
        try:
            data_representation = super().to_representation(data)
            if Members.objects.filter(team=data_representation.get('_id')).exists():
                leader_present = False
                num_of_leader = 0
                members = Members.objects.filter(team=data_representation.get('_id'))
                length_of_member = len(members)

                for i in members:
                    if i.is_leader:
                        num_of_leader += 1
                        leader_present = True

                if leader_present and num_of_leader == 1 and length_of_member <= data_representation.get(
                        'number_of_member'):

                    serializer = Memberserializer(members, many=True)
                    res = {'team': data_representation, 'members': [],"fields":[]}
                    if serializer.data:
                        for member_data in serializer.data:
                            member = Members.objects.get(_id=member_data.get('_id'))
                            application_for_participation = ParticipationSerializer(
                                Participation.objects.filter(member=member),
                                many=True
                            )
                            if application_for_participation.data:
                                response = application_for_participation.data
                                for application_data in response:
                                    # Adjusted usage of FieldSerializer
                                    print(application_data['_id'])
                                    print('form',application_data['form'])
                                    fields_serializer = FieldSerializer({'application_id': application_data['_id'],'form':application_data['form']})
                                    fields_data = fields_serializer.data 
                                    # long = LongSerializer(Longfieldinput.objects.filter(registeration=application_data.get('_id')), many=True).data
                                    
                                    # application_data['fields'].append(long)
                                    application_data['user_id'] = member.user._id
                                    application_data['is_leader'] = member.is_leader
                                    application_data['additional_data'] = fields_data['fields']
                                res['members'].append({member.user.email: response})
                            else:
                                res['members'].append({member.user.email: member.user._id})
                        return res
                    else:
                        return None
                elif not leader_present or num_of_leader > 1 or num_of_leader < 1:
                    return {'error': "there is an issue with the leader"}
                elif length_of_member > data_representation.get('number_of_member'):
                    return {'error': "the number of members is full in this team"}
            else:
                return None
        except Exception as err:
            print(err)
            return err