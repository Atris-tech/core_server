from django.db import models

# Create your models here.
from django.db import models
from start_meeting.models import CreateMeeting

# Create your models here.
class SentimentAnalyzer(models.Model):
    meeting_id = models.ForeignKey(to=CreateMeeting, on_delete=models.CASCADE)
    sentiment = models.TextField(blank=True)
    sentiment_value=models.IntegerField()

    class Meta:
        db_table = "sentiment_analyzer"