from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer
from .models import Team,Members,Teamrequestedmembers
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
        print(app_id)
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
        print('multiple : ',multiple_fields)
        for i in range(len(range_fields)):
            range_fields[i]['type'] = "range"
        for i in range(len(slider_fields)):
            slider_fields[i]['type'] = 'slider'
        for i in range(len(linear_fields)):
            linear_fields[i]['type'] = 'linear'
        for i in range(len(multiple_fields)):
            type = MultipleChoiceField.objects.get(_id = multiple_fields[i]['multiple_field']).type
            multiple_fields[i]['type'] = type
            print(type)
        if long_fields :
            all_fields+=long_fields
        if short_fields : 
            all_fields += short_fields
        if multiple_fields:
            all_fields+=multiple_fields
        if toggle_fields:
            all_fields+=toggle_fields
        if stepper_fields:
            all_fields+=stepper_fields
        if date_fields:
            all_fields+=date_fields
        if slider_fields:
            
            all_fields += slider_fields
        if range_fields:
            all_fields+=range_fields
        if linear_fields:
            all_fields+=linear_fields
        if file_fields:
            all_fields+=file_fields
        if tag_fields:
            all_fields+=tag_fields
        # print('all fields : ',all_fields)
        
        field_map = {field['serial_number']: field for field in all_fields}
        
        for i in range(1, len(field_map.keys())+1):
            
            if 'long_field' in field_map[i].keys():
                print('long from field serializer')
                field_map[i]['type'] = 'long_field'
            if 'short_field' in field_map[i].keys():
                print('short from field serializer')
                field_map[i]['type'] = 'short_field'
            if 'toggle' in field_map[i].keys():
                print('toggle from field serializer')
                field_map[i]['type'] = 'toggle_fields'
            if 'stepper_field' in field_map[i].keys():
                print('stepper from field serializer')
                field_map[i]['type'] = 'stepper_fields'
            if 'date_fields' in field_map[i].keys():
                print('date from field serializer')
                field_map[i]['type'] = 'date_fields'
            if 'file' in field_map[i].keys():
                print('file from field serializer')
                field_map[i]['type'] = 'file_fields'
            if 'tags_field' in field_map[i].keys():
                print('tag from field serializer')
                field_map[i]['type'] = 'tag_fields'
                
                
            if field_map.get(i):
                # print('field with serial number : ',field_map.get(i))
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
            hackathon_id = data_representation.get('hackathon')
            requested_members = Teamrequestedmembers.objects.filter(team = team_id,hackathon = hackathon_id).values('email')
            members_qs = Members.objects.filter(team=team_id)
            members_count = members_qs.count()
            leader_present = members_qs.filter(is_leader=True).count() == 1

            if members_count <= data_representation.get('number_of_member'):
                if leader_present:
                    serializer = Memberserializer(members_qs, many=True)
                    serialized_members = serializer.data
                    # print('serialized members : ',serialized_members)
                    result = {'team': data_representation, 'members': []}
                    # print('result : ',result)
                    # print('serialized members2 : ',serialized_members)
                    for email in requested_members:
                        print(email)
                        try:
                            email = email['email']
                            user = UserProfile.objects.get(email = email)
                            member=Members.objects.get(user=user)
                            participation = Participation.objects.get(member=member)
                            participation_serializer = ParticipationSerializer(participation,many=False)
                            participation_qs = participation_serializer.data
                            participation_qs['college_name'] = user.organisation
                            print('participation : ',participation_qs)
                            
                            application_data=[]
                            fields_serializer = FieldSerializer({'application_id': participation_qs.get('_id'), 'form': participation_qs.get('form')})
                            fields_data = fields_serializer.data['fields']
                                # print(fields_data)
                            application_data.append({
                                        'required_data': participation_qs,
                                        'is_leader': member.is_leader,
                                        'additional_data': fields_data
                                    })
                            result['members'].append({email: application_data})
                            
                        except Participation.DoesNotExist:
                            user = UserProfile.objects.get(email = email)
                            result['members'].append({email : str(user._id)})
                        except UserProfile.DoesNotExist:
                            result['members'].append({email : "pending"})
                        except Exception as e:
                            print(e)
                            return (str(e))
                            
                    # print('result',result)
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
        
class RequestedEmail(ModelSerializer):
    
    class Meta:
        model = Teamrequestedmembers
        fields = '__all__'