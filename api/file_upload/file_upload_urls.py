from django.conf.urls import url
from .file_upload_views import UploadView
urlpatterns = [
  url('upload/', UploadView.as_view(), name='file-upload'),
]
