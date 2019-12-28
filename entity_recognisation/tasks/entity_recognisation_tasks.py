from celery import shared_task
from start_meeting.models import CreateMeeting
from transcribe.models import Transcribe
from entity_recognisation.entityGlobals import EntityGlobals
import requests
import json
from entity_recognisation.models import Recognise
from web_socket.services.RedisDbService import UpdateToRedis
globalObj = EntityGlobals()
redis_obj = UpdateToRedis()

@shared_task()
def entityRecog(meetingId):

        URL = globalObj.getGlobals(key="server")

        meeting_obj = CreateMeeting.objects.get(meeting_id=str(meetingId))
        transcribeobj = Transcribe.objects.filter(meeting_id=meeting_obj)

        task_count = redis_obj.normal_get(key = meetingId)


        #labels is a dictionary
        if int(task_count) == 0:
            print("in if")
            transcribedic = transcribeobj.values()

            to_send_text = ''
            for val in transcribedic:
                to_send_text = to_send_text + ' ' + str(val['text'])
            meeting_obj.text = to_send_text
            meeting_obj.save()
            print(to_send_text)
            params = (
                ('text', to_send_text),
            )
            r = requests.post(
                url=URL,
                params=params
            )
            data = r.text
            newDic = json.loads(data)
            entity_data = newDic["data"]
            Recognise(
                meeting_id=meeting_obj,
                entities=entity_data
            ).save()
            task_count = int(task_count) + 1
            redis_obj.add(key=meetingId, dic =task_count)

        elif int(task_count) == 3:
            print("text")
            to_send_text = meeting_obj.text
            print(to_send_text)
            params = (
                ('text', to_send_text),
            )
            r = requests.post(
                url=URL,
                params=params
            )
            data = r.text
            newDic = json.loads(data)
            entity_data = newDic["data"]
            Recognise(
                meeting_id=meeting_obj,
                entities=entity_data
            ).save()

            task_count = int(task_count) + 1
            redis_obj.add(key=meetingId, dic=task_count)
            CreateMeeting(
                status='complete'
            ).save()


        else:
            to_send_text = meeting_obj.text
            print("in else")
            print("text", to_send_text)
            params = (
                ('text', to_send_text),
            )
            r = requests.post(
                url=URL,
                params=params
            )
            data = r.text
            print("data")
            print(data)
            newDic = json.loads(data)
            entity_data = newDic["data"]
            Recognise(
                meeting_id= meeting_obj,
                entities=entity_data
            ).save()
            task_count = int(task_count) + 1
            redis_obj.add(key=meetingId, dic=task_count)




