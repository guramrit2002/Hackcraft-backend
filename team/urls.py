from django.urls import path
from .views import teampost

urlpatterns = [
    path('',teampost)
]

