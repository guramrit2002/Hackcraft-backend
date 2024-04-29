from django.urls import path
from .views import *

urlpatterns = [
        path('userget/<uid>',userProfile),
        path('userpost',userprofilepost),
        path('userput/<uid>',userprofileput),
        path("isregistered/<email>",isregistered),
        path('otp/<email>',otpsend),
        path('otprecieve',otprecieve),
        path('otpreset/<email>',otpreset),
        path('profilecomplete/<email>',profilecompletepercentage)
    ]
