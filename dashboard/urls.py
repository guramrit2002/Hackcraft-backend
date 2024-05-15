from django.urls import path
from .views import dashboardgetapi,defaultgethackathons

urlpatterns = [
    path('stats/<hackathon>',dashboardgetapi),
    path('gethackathons/<email>',defaultgethackathons)
]
