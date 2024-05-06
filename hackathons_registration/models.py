from django.db import models
from hackathon_template.models import Hackathon
import uuid

# Create your models here.

TYPE_OF_OPTIONS = [
    ('RADIO', 'Radio'),
    ('CHECK', 'Checkbox')
]

class HackathonRegisterationForm(models.Model):
    
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created = models.DateTimeField(auto_now_add=True)
    hackathon = models.ForeignKey(Hackathon,on_delete=models.CASCADE)
    number_of_fields = models.IntegerField(null = True)
    
    def __str__(self):
        return str(self.hackathon)



class ShortAnswerField(models.Model):
    
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created = models.DateTimeField(auto_now_add=True)
    form = models.ForeignKey(HackathonRegisterationForm, on_delete=models.CASCADE)
    serial_number = models.IntegerField(null = True)
    validation  = models.CharField(max_length = 200)
    hint = models.CharField(max_length = 1000)
    label = models.CharField(max_length=500)
    error_text = models.CharField(max_length = 500)
    required = models.BooleanField()
    
    
    def __str__(self) -> str:
        return str(self._id)


class LongAnswerField(models.Model):
    
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created = models.DateTimeField(auto_now_add=True)
    form = models.ForeignKey(HackathonRegisterationForm, on_delete=models.CASCADE)
    serial_number = models.IntegerField(null = True)
    word_limit = models.IntegerField()
    label = models.CharField(max_length=1000)
    error_text = models.CharField(max_length = 500)
    required = models.BooleanField()
    
    
    def __str__(self) -> str:
        return str(self.label)

class DropdownField(models.Model):
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created = models.DateTimeField(auto_now_add=True)
    form = models.OneToOneField(HackathonRegisterationForm, on_delete=models.CASCADE )
    serial_number = models.IntegerField(null = True)
    choices = models.CharField(max_length=20)
    
    def getchoices(self):
        return[choice.strip() for choice in self.choices.split(',')]
    def __str__(self) -> str:
        return str(self._id)


class MultipleChoiceField(models.Model):
    
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created = models.DateTimeField(auto_now_add=True)
    form = models.ForeignKey(HackathonRegisterationForm, on_delete=models.CASCADE)
    serial_number = models.IntegerField(null = True)
    error_text = models.CharField(max_length = 500)
    type = models.CharField(max_length = 20)
    label = models.CharField(max_length=200,null=True)
    required = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return str(self._id)

class Options(models.Model):
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created = models.DateTimeField(auto_now_add=True)
    related = models.CharField(max_length=500, choices = TYPE_OF_OPTIONS, null=True)
    text = models.CharField(max_length = 500)
    serial_number = models.IntegerField()
    field = models.ForeignKey(MultipleChoiceField,on_delete = models.CASCADE)
    def __str__(self) -> str:
        return str(self._id)
    
class Toggle(models.Model):
    
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created = models.DateTimeField(auto_now_add=True)
    form = models.ForeignKey(HackathonRegisterationForm, on_delete=models.CASCADE)
    serial_number = models.IntegerField(null = True)
    label = models.CharField(max_length=500)
    error_text = models.CharField(max_length = 500)
    required = models.BooleanField(default=False)
    
    
    def __str__(self) -> str:
        return str(self._id)

class Stepper(models.Model):
    
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created = models.DateTimeField(auto_now_add=True)
    form = models.ForeignKey(HackathonRegisterationForm, on_delete=models.CASCADE)
    label = models.CharField(max_length=500,null=True)
    serial_number = models.IntegerField(null = True)
    error_text = models.CharField(max_length = 500)
    min_value = models.IntegerField()
    max_value = models.IntegerField()
    required = models.BooleanField(default=False)
    
    def __str__(self)->str:
        return str(self._id)
    

class Date(models.Model):
    
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created = models.DateTimeField(auto_now_add=True)
    form = models.ForeignKey(HackathonRegisterationForm, on_delete=models.CASCADE)
    serial_number = models.IntegerField(null = True)
    label = models.CharField(max_length=100,null=True)
    error_text = models.CharField(max_length = 500)
    min_date = models.DateField()
    max_date = models.DateField()
    required = models.BooleanField(default=False)
    
    def __str__(self)->str:
        return str(self._id)
    
class Slider(models.Model):
    
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created = models.DateTimeField(auto_now_add=True)
    form = models.ForeignKey(HackathonRegisterationForm, on_delete=models.CASCADE)
    serial_number = models.IntegerField(null = True)
    error_text = models.CharField(max_length = 500)
    labels = models.JSONField(default={})
    label = models.CharField(max_length=200,null=True)
    type = models.CharField(max_length = 10, null = True)
    required = models.BooleanField(default=False)
    
    def __str__(self)-> str:
        return str(self._id)
    
class Fileupload(models.Model):
    
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created = models.DateTimeField(auto_now_add=True)
    form = models.ForeignKey(HackathonRegisterationForm, on_delete=models.CASCADE)
    serial_number = models.IntegerField(null = True)
    error_text = models.CharField(max_length = 500)
    hint = models.CharField(max_length = 500)
    label = models.CharField(max_length = 500)
    required = models.BooleanField(default=False)
    
    def __str__(self)-> str:
        return str(self._id)

class Tags(models.Model):
    
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created = models.DateTimeField(auto_now_add=True)
    form = models.ForeignKey(HackathonRegisterationForm, on_delete=models.CASCADE)
    serial_number = models.IntegerField(null = True)
    error_text = models.CharField(max_length = 500)
    label = models.CharField(max_length = 500)
    required = models.BooleanField(default=False)
    
class TagOptions(models.Model):
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length = 500)
    serial_number = models.IntegerField()
    field = models.ForeignKey(Tags,on_delete = models.CASCADE)
    def __str__(self) -> str:
        return str(self._id)
    
class Section(models.Model):
    _id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created = models.DateTimeField(auto_now_add=True)
    form = models.ForeignKey(HackathonRegisterationForm, on_delete=models.CASCADE)
    serial_number = models.IntegerField(null = True)
    section_name = models.CharField(max_length = 500)
    number_of_questions = models.IntegerField()
    
    
    def __str__(self) -> str:
        return self.section_name
    
