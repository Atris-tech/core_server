from django.conf.urls import url
from .api_start_meeting_views import CreateMeetingView
urlpatterns = [
  url('', CreateMeetingView.as_view(), name='start-meeting'),
]