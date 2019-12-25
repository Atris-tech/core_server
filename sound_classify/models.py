# Create your models here.
from django.db import models
from start_meeting.models import CreateMeeting
# Create your models here.
class Classify(models.Model):
    meeting_id = models.ForeignKey(to=CreateMeeting, on_delete=models.CASCADE)
    segment_id = models.IntegerField(blank=False)
    sounds = models.TextField(blank=True)
    class Meta:
        db_table = "classify_sounds"