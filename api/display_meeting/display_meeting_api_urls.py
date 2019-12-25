from django.conf.urls import url
from api.display_meeting.display_meeting_api_views import DisplayMeeting
urlpatterns = [
  url('', DisplayMeeting.as_view(), name='display-meeting'),
]