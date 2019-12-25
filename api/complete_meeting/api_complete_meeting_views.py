from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from complete_meeting.serializers import CompleteMeetingSerializer
from complete_meeting.CompleteMeetingHandler import CompleteMeetingHandler

meetingHandlerobj = CompleteMeetingHandler()

class CompleteMeetingView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        complete_meeting_serializer= CompleteMeetingSerializer(data=request.data)
        if complete_meeting_serializer.is_valid():
            meeting_ID = complete_meeting_serializer.data['meeting_id']
            meetingHandlerobj.meetingHandler(meetingid=meeting_ID)
            return Response(data="success", status=status.HTTP_200_OK)
        else:
            return Response(data=complete_meeting_serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)