from django.urls import path
from .views import dashboardgetapi,defaultgethackathons,dashboardteamget

urlpatterns = [
    path('stats/<hackathon>',dashboardgetapi),
    path('gethackathons/<email>',defaultgethackathons),
    path('dashboardteamget/<hackathon>',dashboardteamget)
]
