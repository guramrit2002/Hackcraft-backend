from django.db import models
import uuid

# Create your models here.

class Skill(models.Model):
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    skill_name = models.CharField(max_length=200,unique=True)
    
    def __str__(self) -> str:
        return self.skill_name
    

class UserProfile(models.Model):
    
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    first_name = models.CharField(max_length=200)
    last_name  = models.CharField(max_length=200)
    email = models.EmailField(max_length=254,unique = True)
    username  = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    organisation = models.CharField(max_length=250)
    cousrse_name = models.CharField(max_length=250)
    course_duration = models.IntegerField()
    date_of_birth = models.DateField()
    interest = models.CharField(max_length=250)
    about  = models.CharField(max_length=3000)
    education_qualification = models.CharField(max_length=100)
    degree_type = models.CharField(max_length=300)
    specialization = models.CharField(max_length=200)
    degree_duration = models.IntegerField()
    percentage = models.IntegerField()
    university_name = models.CharField(max_length=500)
    skill = models.ManyToManyField(Skill,default = None)
    # social links
    facebook = models.CharField(max_length=100)
    x = models.CharField(max_length=50)
    instagram = models.CharField(max_length=100)
    linkedin = models.CharField(max_length=100)
    github = models.CharField(max_length=100)
    medium = models.CharField(max_length=100)
    reddit = models.CharField(max_length=100)
    slack = models.CharField(max_length=100)
    dribble = models.CharField(max_length=100)
    behance = models.CharField(max_length=100)
    codepen = models.CharField(max_length=100)
    figma = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} profile'
    
    def print_model_fields(self):
        res_dict = {}
        for field in self._meta.get_fields():
            
            try:
                field_name = field.name
                if field.many_to_many or field.one_to_many:
                    field_value = ', '.join(str(item) for item in getattr(self, field_name).all())
                else:
                    field_value = getattr(self, field_name)
                res_dict[field_name] = field_value
                
            except Exception as e:
                print(f"Error printing field {field_name}: {e}")
        return res_dict
    

