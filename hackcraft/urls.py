from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('hackathons_registration.urls')),
    path('',include('user.urls')),
    path('team/',include('team.urls')),
    path('participation/',include('user_participation.urls')),
    path('anonymous/',include('anonymous.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

