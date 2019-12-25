from rest_framework import serializers
from .models import CreateMeeting
# a serializer class for our models Upload
class CreateMeetingSerializer(serializers.ModelSerializer):
  class Meta():
    model = CreateMeeting
    # the fields which needs to be serialized
    fields = ('meeting_id', 'group_id')