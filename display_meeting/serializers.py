from rest_framework import serializers

class DisplayMeetingSerializer(serializers.Serializer):
   meeting_id = serializers.CharField()