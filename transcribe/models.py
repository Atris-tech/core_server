from django.db import models

# Create your models here.
from django.db import models
from start_meeting.models import CreateMeeting

# Create your models here.
class Transcribe(models.Model):
    meeting_id = models.ForeignKey(to=CreateMeeting, on_delete=models.CASCADE)
    segment_id = models.IntegerField(blank=False)
    text = models.TextField(blank=False)

    class Meta:
        db_table = "transcribe_text"