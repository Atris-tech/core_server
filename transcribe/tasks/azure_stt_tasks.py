from __future__ import absolute_import, unicode_literals
from celery import shared_task
import azure.cognitiveservices.speech as speechsdk
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from start_meeting.models import CreateMeeting
from transcribe.models import Transcribe
layer = get_channel_layer()

@shared_task
def azure_stot(meetingId, newFile, segment):
    print(segment)
    print("meetingid")
    print(meetingId)
    meeting_obj = CreateMeeting.objects.get(meeting_id = str(meetingId))

    value = str(meeting_obj.group_id)
    print("value")
    print(value)

    speech_key, service_region = "ac8b9913a547447c84102cc2a9a26059", "centralindia"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Creates an audio configuration that points to an audio file.
    # Replace with your own audio filename.
    audio_filename = newFile
    audio_input = speechsdk.AudioConfig(filename=audio_filename)

    # Creates a recognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    print("speech recognize")

    print(speech_recognizer)

    print("Recognizing first result...")

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
            print("segment", segment)
            print("text", result.text)
            transcribeObj = Transcribe(
                meeting_id= meeting_obj,
                segment_id= segment,
                text= result.text
            )
            status = transcribeObj.save()
            print("saved to db", status)
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
            return (result.text)
        elif result.reason == speechsdk.ResultReason.NoMatch:
            raise Exception
            # print("No speech could be recognized: {}".format(result.no_match_details))
            # return result.no_match_details
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))

            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                return cancellation_details.error_details
    except Exception as e:
        s = "<silent audio>"
        return s

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))

        async_to_sync(layer.group_send)(
            value, {
                'type': 'send_toSocket',
                'message': result.text
            }
        )
        return (result.text)
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
        return result.no_match_details
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))

        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            return cancellation_details.error_details

