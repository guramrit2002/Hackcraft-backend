from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(HackathonRegisterationForm)
admin.site.register(ShortAnswerField)
admin.site.register(LongAnswerField)
admin.site.register(MultipleChoiceField)
admin.site.register(DropdownField)
admin.site.register(OptionDropdown)
admin.site.register(Toggle)
admin.site.register(Stepper)
admin.site.register(Date)
admin.site.register(File)
admin.site.register(Tags)
admin.site.register(Section)
admin.site.register(Options)
admin.site.register(Slider)
admin.site.register(TagOptions)