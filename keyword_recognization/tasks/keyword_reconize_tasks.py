from celery import shared_task
from start_meeting.models import CreateMeeting
from transcribe.models import Transcribe
import requests
import json
from keyword_recognization.models import KeywordRecognize
from keyword_recognization.keywordGlobals import KeywordGlobals
globalObj = KeywordGlobals()

@shared_task()
def keywordRecog(meetingId):
    URL = globalObj.getGlobals(key="server")

    meeting_obj = CreateMeeting.objects.get(meeting_id=str(meetingId))
    transcribeobj = Transcribe.objects.filter(meeting_id=meeting_obj)
    task_count = meeting_obj.count
    # labels is a dictionary
    if task_count == 0:
        transcribedic = transcribeobj.values()

        to_send_text = ''
        for val in transcribedic:
            to_send_text = to_send_text + ' ' + str(val['text'])
        task_count = task_count + 1
        CreateMeeting(
            count=task_count,
            text=to_send_text
        ).save()
        params = (
            ('text', to_send_text),
        )
        r = requests.post(
            url=URL,
            params=params
        )
        data = r.text
        newDic = json.loads(data)
        keyword_data = newDic["data"]
        KeywordRecognize(
            meeting_id=meeting_obj,
            keywords=keyword_data
        ).save()


    elif task_count == 3:
        to_send_text = meeting_obj.text
        params = (
            ('text', to_send_text),
        )
        r = requests.post(
            url=URL,
            params=params
        )
        data = r.text
        newDic = json.loads(data)
        keyword_data = newDic["data"]
        KeywordRecognize(
            meeting_id=meeting_obj,
            keywords=keyword_data
        ).save()
        task_count = task_count + 1
        CreateMeeting(
            count=task_count,
            status='complete'
        ).save()

    else:
        to_send_text = meeting_obj.text
        params = (
            ('text', to_send_text),
        )
        r = requests.post(
            url=URL,
            params=params
        )
        data = r.text
        newDic = json.loads(data)
        keyword_data = newDic["data"]
        KeywordRecognize(
            meeting_id=meeting_obj,
            keywords=keyword_data
        ).save()
        task_count = task_count + 1
        CreateMeeting(
            count=task_count,
        ).save()