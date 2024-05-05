from django.urls import path
from .views import *
# from .views import teamsget

urlpatterns = [
    path('usertype/<email>',usertype)
    # path("/", .as_view(), name="")
]
