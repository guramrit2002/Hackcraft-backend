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
    

    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type = models.CharField(max_length=500, choices=USER_TYPE,default=' ', null=True,blank=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=250, default=' ' )
    gender = models.CharField(max_length=250, default=' ' )
    city = models.CharField(max_length=250, default=' ' )
    organisation = models.CharField(max_length=250, default=' ' )
    cousrse_name = models.CharField(max_length=250, default=' ' )
    course_end_year = models.IntegerField(default=-1 )
    date_of_birth = models.DateField(null=True)
    interest = models.JSONField(default={} )
    about = models.CharField(max_length=3000, default=' ' )
    education_qualification = models.CharField(max_length=100, default=' ' )
    specialization = models.CharField(max_length=200, default=' ' )
    percentage = models.IntegerField(default=-1 )
    skill = models.ManyToManyField(Skill, default=None,blank=True)
    degree = models.CharField(max_length=200, default=' ' )
    # social links
    facebook = models.CharField(max_length=100, default=' ' )
    x = models.CharField(max_length=50, default=' ' )
    instagram = models.CharField(max_length=100, default=' ')
    linkedin = models.CharField(max_length=100, default=' ' )
    github = models.CharField(max_length=100, default=' ' )
    medium = models.CharField(max_length=100, default=' ' )
    reddit = models.CharField(max_length=100, default=' ' )
    slack = models.CharField(max_length=100, default=' ' )
    dribble = models.CharField(max_length=100, default=' ' )
    behance = models.CharField(max_length=100, default=' ' )
    codepen = models.CharField(max_length=100, default=' ' )
    figma = models.CharField(max_length=100, default=' ' )
    phone = models.CharField(max_length=10, null=True, default=' ' )

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} profile'

        super().save(*args, **kwargs)
    
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
