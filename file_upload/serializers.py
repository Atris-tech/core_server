from rest_framework import serializers
from .models import Upload
# a serializer class for our models Upload
class UploadSerializer(serializers.ModelSerializer):
  class Meta():
    model = Upload
    # the fields which needs to be serialized
    fields = ('file', 'meeting_id', 'timestamp')