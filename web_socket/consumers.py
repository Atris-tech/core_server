from channels.generic.websocket import WebsocketConsumer
import json
import time
import uuid
from asgiref.sync import async_to_sync
from start_meeting.models import CreateMeeting
from transcribe.tasks.azure_stt_tasks import azure_stot
from sound_classify.tasks.ibm_sound_classifier import soundClassifier

t_end = time.time() + 10


class AtrisConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print("websocket connected")
        self.count = -1
        self.group_id = None
        self.meeting_id = None

    def receive (self, text_data=None, bytes_data= None):
        self.count = self.count + 1

        if text_data:
            self.meeting_id = str(text_data)
            print("meeting id", self.meeting_id)
            print("group id", self.group_id)
            qm_obj = CreateMeeting.objects.get(meeting_id=text_data)
            value = str(qm_obj.group_id)
            self.group_id = value

            print("channel created", self.group_id)
            async_to_sync(self.channel_layer.group_add)(
                self.group_id,
                self.channel_name
            )
            print("channel created")

        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        if bytes_data:
            self.new(id = self.meeting_id, data=bytes_data, count = self.count)
        print(self.count)
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_id,
            self.channel_name
        )
        print("disconnected")
    def new(self, data, id, count):
        audFile = "output/"+str(uuid.uuid4())+".wav"
        with open(audFile, mode='bx') as f:
            f.write(data)

        """Call azure script and send newFile"""
        print("id")
        print(id)
        transcribed_text=''
        azure_stot.delay(segment = count, meetingId = id, newFile =audFile)
        soundClassifier.delay(segment = count, meetingId = id, newFile = audFile)

        # """Call google script and send newFile"""
        #
        # """Call IBm Script here and send newFile"""
        #
        # sentiment_dict=IBMobj.soundClassidfier(audFile)
        #
        # finalDic = {
        #     'metting_id': "meeting_id",
        #     'text' : transcribed_text,
        #     'sound' : sentiment_dict
        # }
        # print(finalDic)
        # self.send(text_data=json.dumps(finalDic))
        #
        #
        # self.send(text_data=json.dumps({
        #     'metting_id': "meeting_id",
        #     'text' : transcribed_text,
        #     'sound' : sentiment_dict
        # }))
    def send_toSocket(self, event):
    # function to send data to socket
        print("in socket func")
        self.send(
            text_data=json.dumps({
            'message': event
        }))

#'Diarization' : g_response
