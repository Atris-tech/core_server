from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from display_meeting.serializers import DisplayMeetingSerializer
from display_meeting.DisplayMeetingFacade import DisplayMeetingFacade

meetingFacadeObj = DisplayMeetingFacade

class DisplayMeeting(APIView):
    def get(self, request):
        meeting_serializer = DisplayMeetingSerializer(data=request.data)
        print(request.data)
        if meeting_serializer.is_valid():
            meeting_id = meeting_serializer.data["meeting_id"]
            respData = meetingFacadeObj.getData(meeting_id)
            return Response(data=respData, status=status.HTTP_200_OK)
        else:
            # if file serializers has errors i.e all the valid parameters are not supplied!
            return Response(meeting_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
