from rest_framework import serializers

class CompleteMeetingSerializer(serializers.Serializer):
   meeting_id = serializers.CharField()