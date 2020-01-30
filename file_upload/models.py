from django.db import models
import uuid
import os
from start_meeting.models import CreateMeeting

# the below function will create a unique folder and store the uploaded file in it
def get_file_path(instance, filename):
    filename = "media/"+ str(uuid.uuid4()) + "/" + str(uuid.uuid4()) + filename
    print(filename)
    return os.path.join('', filename)

class Upload(models.Model):
    # calls the get_file_path functions and pass the file instance to it
  file = models.FileField(upload_to=get_file_path,
                          null=True,
                          blank=True,)
  meeting_id = models.TextField(blank=False)
  file_url = models.TextField(blank=False)
  timestamp = models.DateTimeField(auto_now_add=True)
  waveform=models.TextField(blank=False)

  class Meta:
    db_table = "file-url"