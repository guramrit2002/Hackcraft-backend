from django.urls import path
from .views import *
from hackathon_template.views import *

urlpatterns = [
    path('',gethackathon,name="hackathon"),
    path('default/<uuid:id>',defaultpage,name="hackathon"),
    path("default/new", defaultpost, name="new-hackathon"),
    path('form/',hackathon_regiteration_form_get,name="GetHackathon"),
    path('form/<uuid:id>',hackathon_regiteration_form_get_specific,name="GetSpecificHackathon"),
    path("form/create", hackathon_registeration_form_post, name="PostHackathonForm")
]
