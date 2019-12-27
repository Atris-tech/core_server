from celery import shared_task
from start_meeting.models import CreateMeeting
from transcribe.models import Transcribe
import requests
import json
from sentiment_analyzer.models import SentimentAnalyzer
from sentiment_analyzer.sentimentGlobals import SentimentGlobals
globalObj = SentimentGlobals()

@shared_task()
def sentimentAnalyzer(meetingId):
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
        x = r.text
        res = x.strip('][').split(', ')
        sentiments = res[0]
        sentiments_dic = json.loads(sentiments)
        sentiment_data=sentiments_dic["_value"]
        sentiment_value=sentiments_dic["_score"]


        SentimentAnalyzer(
            meeting_id=meeting_obj,
            sentiment=sentiment_data,
            sentiment_value=sentiment_value


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
        x = r.text
        res = x.strip('][').split(', ')
        sentiments = res[0]
        sentiments_dic = json.loads(sentiments)
        sentiment_data = sentiments_dic["_value"]
        sentiment_value = sentiments_dic["_score"]

        SentimentAnalyzer(
            meeting_id=meeting_obj,
            sentiment=sentiment_data,
            sentiment_value=sentiment_value

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
        x = r.text
        res = x.strip('][').split(', ')
        sentiments = res[0]
        sentiments_dic = json.loads(sentiments)
        sentiment_data = sentiments_dic["_value"]
        sentiment_value = sentiments_dic["_score"]

        SentimentAnalyzer(
            meeting_id=meeting_obj,
            sentiment=sentiment_data,
            sentiment_value=sentiment_value

        ).save()
        task_count = task_count + 1
        CreateMeeting(
            count=task_count,
        ).save()