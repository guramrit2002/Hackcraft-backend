from django.urls import path
from .views import teampost,memberpost

urlpatterns = [
    path('',teampost),
    path('member',memberpost)
]

