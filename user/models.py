from django.db import models
import uuid
from django.utils import timezone
import hashlib
import secrets
# Create your models here.
USER_TYPE = (
    ('student','student'),
    ('professional','professional')
)
class Skill(models.Model):
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    skill_name = models.CharField(max_length=200,unique=True)
    
    def __str__(self) -> str:
        return str(self._id)
    

class UserProfile(models.Model):
    
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    user_type = models.CharField(max_length=500,choices=USER_TYPE,null=True)
    first_name = models.CharField(max_length=200, null=False)
    last_name  = models.CharField(max_length=200, null=False)
    email = models.EmailField(max_length=254,unique = True, null=False)
    username  = models.CharField(max_length=250, default = ' ',blank=True)
    gender = models.CharField(max_length=250,default = ' ',blank=True)
    city = models.CharField(max_length=250,default = ' ',blank=True)
    organisation = models.CharField(max_length=250,default = ' ',blank=True)
    cousrse_name = models.CharField(max_length=250,default = ' ',blank=True)
    course_end_year = models.IntegerField(default = -1,blank=True)
    date_of_birth = models.DateField(blank=True, null=True,auto_now_add=False)
    interest = models.JSONField(default={},blank=True)
    about  = models.CharField(max_length=3000,default = ' ',blank=True)
    education_qualification = models.CharField(max_length=100,default = ' ',blank=True)
    specialization = models.CharField(max_length=200,default = ' ',blank=True)
    percentage = models.IntegerField(default = -1,blank=True)
    skill = models.ManyToManyField(Skill,default = None,blank=True)
    degree = models.CharField(max_length=200,null=True,default=' ',blank = True)
    # social links
    facebook = models.CharField(max_length=100,default = ' ',blank=True)
    x = models.CharField(max_length=50,default = ' ',blank=True)
    instagram = models.CharField(max_length=100,default = ' ',blank=True)
    linkedin = models.CharField(max_length=100,default = ' ',blank=True)
    github = models.CharField(max_length=100,default = ' ',blank=True)
    medium = models.CharField(max_length=100,default = ' ',blank=True)
    reddit = models.CharField(max_length=100,default = ' ',blank=True)
    slack = models.CharField(max_length=100,default = ' ',blank=True)
    dribble = models.CharField(max_length=100,default = ' ',blank=True)
    behance = models.CharField(max_length=100,default = ' ',blank=True)
    codepen = models.CharField(max_length=100,default = ' ',blank=True)
    figma = models.CharField(max_length=100,default = ' ',blank=True)
    phone = models.CharField(max_length=10,null=True,default=' ',blank=True)
    
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
    



class OTP(models.Model):
    
    user_email = models.EmailField(null=True)
    otp = models.CharField(max_length=128)  # Store hashed OTP
    salt = models.CharField(max_length=64)  # Store salt used for hashing
    created_at = models.DateTimeField(default=timezone.now)
    expiration_minutes = models.IntegerField(default=5)  # Adjust expiration time as needed

    @classmethod
    def  generate_otp(cls,email):
        otp = str(secrets.randbelow(10**6)).zfill(6)  # Generate a 6-digit OTP
        salt = secrets.token_hex(16)  # Generate a random salt
        otp_hash = hashlib.sha256((otp + salt).encode()).hexdigest()  # Hash OTP with salt
        otp_instance = cls.objects.create(otp=otp_hash, salt=salt,user_email = email)
        return {'otp':otp,"otp_id":otp_instance.id}

    def validate_otp(self, otp):
        if self.is_expired():
            return False
        otp_hash = hashlib.sha256((otp + self.salt).encode()).hexdigest()  # Hash provided OTP with salt
        return otp_hash == self.otp

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=self.expiration_minutes)
