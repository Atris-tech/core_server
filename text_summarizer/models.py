
# Create your models here.
from django.db import models
from start_meeting.models import CreateMeeting

# Create your models here.
class TextSummarizer(models.Model):
    meeting_id = models.ForeignKey(to=CreateMeeting, on_delete=models.CASCADE)
    summary = models.TextField(blank=True)

    class Meta:
        db_table = "text_summarizer"