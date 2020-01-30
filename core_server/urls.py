 #mysite/urls.py
from django.conf.urls import include
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('start/', include('api.start_meeting.api_start_meeting_urls')),
    path('meetings/', include('api.display_meeting.display_meeting_api_urls')),
    path('complete/', include('api.complete_meeting.api_complete_meeting_urls')),
    path('audio/', include('api.file_upload.file_upload_urls')),
]