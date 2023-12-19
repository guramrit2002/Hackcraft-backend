from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Hackathon)
admin.site.register(HackathonRegisterationForm)
admin.site.register(CustomField)
admin.site.register(ShortAnswerField)
admin.site.register(LongAnswerField)
admin.site.register(MultipleChoiceField)
admin.site.register(DropdownField)

