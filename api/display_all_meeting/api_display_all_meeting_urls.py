from django.conf.urls import url
from api.display_all_meeting.api_display_all_meeting_views import DisplayAllMeeting
urlpatterns = [
  url('', DisplayAllMeeting.as_view(), name='display-meeting'),
]