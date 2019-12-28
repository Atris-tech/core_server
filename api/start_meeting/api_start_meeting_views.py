from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from start_meeting.serializers import CreateMeetingSerializer
from start_meeting.models import CreateMeeting
from web_socket.services.RedisDbService import UpdateToRedis

redisobj = UpdateToRedis()
to_update_meeting_dic = {
            "count_m" : 0,
            "count_ct" : 0,
            "count_cs": 0
        }


class CreateMeetingView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        create_meeting_serializer = CreateMeetingSerializer(data=request.data)

        if create_meeting_serializer.is_valid():

            # Check if every data is valid with the required api parameters (models)
            create_meeting_serializer.save()
            print(create_meeting_serializer.data)

            meeting_response = {
                "meeting_id": create_meeting_serializer.data["meeting_id"],
                "status" : "started"
            }
            q_obj = CreateMeeting.objects.get(
                meeting_id=create_meeting_serializer.data["meeting_id"]
            )
            q_obj.status = 'started'
            q_obj.save()
            redisobj.add(key=create_meeting_serializer.data["meeting_id"], dic=to_update_meeting_dic)
            return Response(
                data=meeting_response,
                status = status.HTTP_200_OK
            )



