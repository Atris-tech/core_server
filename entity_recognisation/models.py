from django.db import models
from start_meeting.models import CreateMeeting

# Create your models here.
class Recognise(models.Model):
    meeting_id = models.ForeignKey(to=CreateMeeting, on_delete=models.CASCADE)
    entities = models.TextField(blank=True)

    class Meta:
        db_table = "entity_recognisation"