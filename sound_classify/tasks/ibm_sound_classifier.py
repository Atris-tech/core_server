from __future__ import absolute_import, unicode_literals
from celery import shared_task
import requests
import json
from start_meeting.models import CreateMeeting
from sound_classify.models import Classify
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

layer = get_channel_layer()

@shared_task()
def soundClassifier(meetingId, newFile, segment):
    print(segment)
    print("meetingid")
    print(meetingId)
    meeting_obj = CreateMeeting.objects.get(meeting_id=str(meetingId))

    value = str(meeting_obj.group_id)
    print("value")
    print(value)
    url = "http://0.0.0.0:5000/model/predict?start_time=0"

    f = open(newFile, 'rb')

    # print(f)

    params = (
        ('start_time', '0'),
    )

    r = requests.post(
        url,
        files={
            "audio": f
        },
        params=params
    )
    sound_dict = {
    }

    test_array = []



    res = json.loads(r.text)




    for item in res['predictions']:


        if item["probability"] >= 0.2:

            intermediate = {
                "labels" : item["label"],
                "probability": item["probability"]
            }
            test_array.append(intermediate)
    finalDic = {
        "result" : test_array
    }



    print(finalDic)

    soundObj = Classify(
        meeting_id=meeting_obj,
        segment_id=segment,
        sounds=finalDic
    )
    status = soundObj.save()
    print("saved to db", status)
    toSendDic = {
        "segment": segment,
        "sounds": finalDic
    }
    async_to_sync(layer.group_send)(
        value, {
            'type': 'send_toSocket',
            'message': toSendDic
        }
    )
    return sound_dict

        # print(r.text)