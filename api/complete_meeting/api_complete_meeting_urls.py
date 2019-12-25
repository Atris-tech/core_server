from django.conf.urls import url
from .api_complete_meeting_views import CompleteMeetingView
urlpatterns = [
  url('', CompleteMeetingView.as_view(), name='start-meeting'),
]