 #mysite/urls.py
from django.conf.urls import include
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('start/', include('api.start_meeting.api_start_meeting_urls')),
    path('meetings/', include('api.display_meeting.display_meeting_api_urls'))
]