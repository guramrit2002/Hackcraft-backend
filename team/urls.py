from django.urls import path
from .views import teampost,memberpost,get_participation_by_hackathons,usertype

urlpatterns = [
    path('',teampost),
    path('member',memberpost),
    path('<team_id>',get_participation_by_hackathons),
    path('usertype/<email>/<hackathon>',usertype)
]

