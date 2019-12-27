from django.db import models

# Create your models here.
from django.db import models
from start_meeting.models import CreateMeeting

# Create your models here.
class KeywordRecognize(models.Model):
    meeting_id = models.ForeignKey(to=CreateMeeting, on_delete=models.CASCADE)
    keywords = models.TextField(blank=True)

    class Meta:
        db_table = "keyword_recognization"