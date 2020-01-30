from __future__ import absolute_import, unicode_literals
from celery import shared_task
import azure.cognitiveservices.speech as speechsdk
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from start_meeting.models import CreateMeeting
from transcribe.models import Transcribe
from web_socket.services.RedisDbService import UpdateToRedis

redis_obj = UpdateToRedis()
layer = get_channel_layer()

@shared_task
def azure_stot(meetingId, newFile, segment):
    # print(segment)
    # print("meetingid")
    # print(meetingId)
    meeting_obj = CreateMeeting.objects.get(meeting_id = str(meetingId))

    value = str(meeting_obj.group_id)
    # print("value")
    # print(value)

    speech_key, service_region = "c75ee69395f040baa9801ce00134030e", "eastus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Creates an audio configuration that points to an audio file.
    # Replace with your own audio filename.
    audio_filename = newFile
    audio_input = speechsdk.AudioConfig(filename=audio_filename)

    # Creates a recognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    # print("speech recognize")
    #
    # print(speech_recognizer)

    print("Recognizing"+str(segment) +" result...")

    # Starts speech recognition, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed.  The task returns the recognition text as result.
    # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
    # shot recognition like command or query.
    # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    result = speech_recognizer.recognize_once()

    # Checks result.

    try:
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            # print("Recognized: {}".format(result.text))
            # print("segment", segment)
            # print("text", result.text)
            transcribeObj = Transcribe(
                meeting_id= meeting_obj,
                segment_id= segment,
                text= result.text
            )
            status = transcribeObj.save()
            #print("saved to db", status)
            toSendDic = {
                "segment" : segment,
                "text" : result.text
            }
            async_to_sync(layer.group_send)(
                value, {
                    'type': 'send_toSocket',
                    'message' : toSendDic
                }
            )
            to_check_dic = redis_obj.get_data(key=meetingId)
            #print(to_check_dic)
            x = int(to_check_dic["count_ct"])
            print(type(x))
            to_check_dic["count_ct"] = x + 1
            redis_obj.add(key=meetingId, dic=to_check_dic)
        elif result.reason == speechsdk.ResultReason.NoMatch:

            raise Exception
            # print("No speech could be recognized: {}".format(result.no_match_details))
            # return result.no_match_details
        elif result.reason == speechsdk.ResultReason.Canceled:
            to_check_dic = redis_obj.get_data(key=meetingId)
            #print(to_check_dic)
            to_check_dic["count_ct"] = int(to_check_dic["count_ct"]) + 1
            redis_obj.add(key=meetingId, dic=to_check_dic)
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))

            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                return cancellation_details.error_details
    except Exception as e:
        s = "<silent audio>"
        to_check_dic = redis_obj.get_data(key=meetingId)
        print(to_check_dic)
        x = int(to_check_dic["count_ct"])
        print(type(x))
        to_check_dic["count_ct"] = x + 1
        redis_obj.add(key=meetingId, dic=to_check_dic)
        return s


