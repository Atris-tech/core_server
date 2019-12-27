from celery import shared_task
from start_meeting.models import CreateMeeting
from transcribe.models import Transcribe
import requests
import json
from text_summarizer.models import TextSummarizer
from text_summarizer.SummarizerGlobals import SummarizerGlobals
globalObj = SummarizerGlobals()

@shared_task()
def textSummarizer(meetingId):
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
        summary_data = newDic["data"]
        TextSummarizer(
            meeting_id=meeting_obj,
            summary=summary_data
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
        summary_data = newDic["data"]
        TextSummarizer(
            meeting_id=meeting_obj,
            summary=summary_data
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
        summary_data = newDic["data"]
        TextSummarizer(
            meeting_id=meeting_obj,
            summary=summary_data
        ).save()
        task_count = task_count + 1
        CreateMeeting(
            count=task_count,
        ).save()


