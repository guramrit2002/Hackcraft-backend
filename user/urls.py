from django.urls import path
from .views import *

urlpatterns = [
    path('userget/<uid>',userProfile),
    path('userpost',userprofilepost),
    path('userput/<uid>',userprofileput)
]
