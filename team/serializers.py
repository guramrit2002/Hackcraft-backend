from rest_framework.serializers import ModelSerializer
# from .models import Team,Members
# from user_participation.serializers import ParticipationSerializer 
# from user_participation.models import Participation

# class Memberserializer(ModelSerializer):
    
#     class Meta:
#         model = Members
#         fields = '__all__'
        
# class Teamserializer(ModelSerializer) :
    
#     class Meta:
#         model = Team
#         fields = '__all__'
    
#     def to_representation(self, data):
#         try:
#             data_representation = super().to_representation(data)
#             if Members.objects.filter(team=data_representation.get('_id')).exists():
#                 leader_present = False
#                 num_of_leader = 0
#                 members = Members.objects.filter(team=data_representation.get('_id'))
#                 length_of_member = len(members)
                
#                 for i in members:
#                     if i.is_leader :
#                         num_of_leader += 1
#                         leader_present = True
#                 print(leader_present)
#                 print(num_of_leader)
#                 print(data_representation.get('number_of_member'))
#                 print(length_of_member)
#                 if leader_present and num_of_leader == 1 and length_of_member<=data_representation.get('number_of_member'):
                    
#                     serializer = Memberserializer(members, many=True)
#                     res = {'team': data_representation, 'members': []}
#                     if serializer.data:
#                         for member_data in serializer.data:
#                             member = Members.objects.get(_id=member_data.get('_id'))
#                             application_for_participation = ParticipationSerializer(
#                                 Participation.objects.filter(member=member),
#                                 many=True
#                             )
#                             if application_for_participation.data:
#                                 response = application_for_participation.data
#                                 for application_data in response:
#                                     application_data['user_id'] = member.user._id
#                                     application_data['is_leader'] = member.is_leader
#                                 res['members'].append({member.user.email: response})
#                             else:
#                                 res['members'].append({member.user.email: member.user._id})
#                         return res
#                     else:
#                         return None
#                 elif not leader_present or num_of_leader>1 or num_of_leader<1:
#                     return {'error':"there is issue with leader"}
#                 elif length_of_member > data_representation.get('number_of_member'):
#                     return {'error':"number of members are full in this team"}
#             else:
#                 return None
#         except Exception as err:
#             print(err)
#             return err


