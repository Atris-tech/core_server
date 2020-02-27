from channels.generic.websocket import WebsocketConsumer
import json
import time
import uuid
from asgiref.sync import async_to_sync
from start_meeting.models import CreateMeeting
from transcribe.tasks.azure_stt_tasks import azure_stot
from sound_classify.tasks.ibm_sound_classifier import soundClassifier
from .services.RedisDbService import UpdateToRedis
from entity_recognisation.tasks.entity_recognisation_tasks import entityRecog
from keyword_recognization.tasks.keyword_reconize_tasks import keywordRecog
from text_summarizer.tasks.text_summarizer_tasks import textSummarizer
from sentiment_analyzer.tasks.sentiment_analyzer_tasks import sentimentAnalyzer
# import base64

redis_obj = UpdateToRedis()

t_end = time.time() + 10


class AtrisConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print("websocket connected")
        self.count = -1
        self.group_id = None
        self.meeting_id = None



    def receive (self, text_data=None, bytes_data= None):


        if text_data:

            if "status" in text_data :
                completion_dic = json.loads(text_data)
                meeting_id_key_val = completion_dic["meetingID"]
                print("status", completion_dic["status"])


                #encoded_string = completion_dic["audio"]
               # print(encoded_string)
                #str_audio = base64.b64decode(str(base64.b64encode(encoded_string)))
                #print(str_audio)
                #print(str_audio)
                #print(type(str_audio))
                #decoded_audio = base64.decodebytes(str_audio)
                #print(decoded_audio)
                #print(type(decoded_audio))
                # with open("output/audFile.wav", mode='bx') as f:
                #     f.write(str_audio)

                print("before meeting dic")
                meeting_dic = redis_obj.get_data(key = str(meeting_id_key_val))
                #print(meeting_dic)
                while meeting_dic["count_m"] != meeting_dic["count_ct"] and \
                        meeting_dic["count_m"] != meeting_dic["count_cs"]:
                    meeting_dic = redis_obj.get_data(key=meeting_id_key_val)

                print("meeting Dic", meeting_dic)
                print("done bro")
                redis_obj.add(key=meeting_id_key_val, dic=0)
                # entityRecog.delay(meetingId=meeting_id_key_val)
                # keywordRecog.delay(meetingId=meeting_id_key_val)
                # textSummarizer.delay(meetingId=meeting_id_key_val)
                # sentimentAnalyzer.delay(meetingId=meeting_id_key_val)

            else:
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


        if bytes_data:
            self.count = self.count + 1
            self.new(id = self.meeting_id, data=bytes_data, count = self.count)
            meeting_dic_to_update_check = redis_obj.get_data(key=self.meeting_id)
            meeting_dic_to_update_check["count_m"] = meeting_dic_to_update_check["count_m"] + 1
            #print("updating dic", meeting_dic_to_update_check)
            redis_obj.add(key = self.meeting_id, dic=meeting_dic_to_update_check)
        #print(self.count)
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
        #print("id")
        #print(id)
        transcribed_text=''
        azure_stot.delay(segment = count, meetingId = id, newFile =audFile)
        soundClassifier.delay(segment = count, meetingId = id, newFile = audFile)


    def send_toSocket(self, event):
    # function to send data to socket
        print("in socket func")
        #print(str(event))
        self.send(
            text_data=json.dumps({
            'message': event
        }))

#'Diarization' : g_response
