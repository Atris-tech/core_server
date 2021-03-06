from start_meeting.models import CreateMeeting
from transcribe.models import Transcribe
from sound_classify.models import Classify
from entity_recognisation.models import Recognise
from keyword_recognization.models import KeywordRecognize
from sentiment_analyzer.models import SentimentAnalyzer
from text_summarizer.models import TextSummarizer
from file_upload.models import Upload
class DisplayMeetingFacade:
    def getData(meetingID):
        createMeetingObj = CreateMeeting.objects.get(meeting_id = meetingID)
        transcribeObj = Transcribe.objects.filter(meeting_id = createMeetingObj)
        classifyObj =  Classify.objects.filter(meeting_id = createMeetingObj)
        entityObj = Recognise.objects.get(meeting_id=createMeetingObj)
        entityDic = entityObj.entities
        transcribeDic = transcribeObj.order_by('segment_id').values()
        classifyDic = classifyObj.order_by('segment_id').values()
        keywordObj=KeywordRecognize.objects.get(meeting_id=createMeetingObj)
        keywordDic = keywordObj.keywords
        summaryObj=TextSummarizer.objects.get(meeting_id=createMeetingObj)
        summaryDic=summaryObj.summary
        sentimentObj=SentimentAnalyzer.objects.get(meeting_id=createMeetingObj)
        fileURLObj=Upload.objects.get(meeting_id=meetingID)
        URLDic = fileURLObj.file_url
        audioWaveform= fileURLObj.waveform


    # url = File
        sentimentDic=sentimentObj.sentiment
        fullText = createMeetingObj.text

        finalDic = {}
        finalArray = []
        count = 0
        for val1, val2 in zip(transcribeDic, classifyDic):
            newSegment = "Segment_" + str(count)
            finalArray.append(

                {
                    "text": val1["text"],
                    "sound": val2["sounds"]
                }

            )
            count = count + 1

            finalDic = {
                "fullText" : fullText,
                "entities": entityDic,
                "transcribe" : finalArray,
                "keywords":keywordDic,
                "summarizer":summaryDic,
                "sentiment":sentimentDic,
                "file_url":URLDic,
                "audio_waveform":audioWaveform


            }




        return finalDic
