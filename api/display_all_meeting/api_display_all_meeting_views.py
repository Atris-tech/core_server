from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from start_meeting.models import CreateMeeting
from display_all_meeting.DisplayAllFacade import DisplayAllMeetingFacade

meetingFacadeObj = DisplayAllMeetingFacade

class DisplayAllMeeting(APIView):
    def get(self, request):
            meetingObj = CreateMeeting.objects.all()
            allMeetingData = meetingObj.values()
            dataToSend = []
            for meeting in allMeetingData:
                meetingid = meeting["meeting_id"]
                print(meetingid)
                meetingData = DisplayAllMeetingFacade.getData(meetingID =meetingid)
                dataToSend.append(meetingData)


            return Response(data=dataToSend, status=status.HTTP_200_OK)
