from django.db import models


# Create your models here.
class CreateMeeting(models.Model):
    text= models.TextField(blank=False)
    meeting_id = models.CharField(max_length=40, blank=False)
    meeting_name = models.TextField(blank=False, default="meeting 1")
    group_id = models.CharField(max_length=40, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30)

    class Meta:
        db_table = "meetings"