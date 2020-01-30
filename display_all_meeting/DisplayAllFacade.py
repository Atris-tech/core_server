from start_meeting.models import CreateMeeting
from keyword_recognization.models import KeywordRecognize
from text_summarizer.models import TextSummarizer
from file_upload.models import Upload
class DisplayAllMeetingFacade:
    def getData(meetingID):
        createMeetingObj = CreateMeeting.objects.get(meeting_id = meetingID)
        date = createMeetingObj.timestamp
        meeting_name = createMeetingObj.meeting_name
        keywordObj=KeywordRecognize.objects.get(meeting_id=createMeetingObj)
        keywordDic = keywordObj.keywords
        summaryObj=TextSummarizer.objects.get(meeting_id=createMeetingObj)
        summaryDic=summaryObj.summary
        fileURLObj=Upload.objects.get(meeting_id=meetingID)
        URLDic = fileURLObj.file_url
        audioWaveform= fileURLObj.waveform

        finalDic = {
            "meeting_id" : meetingID,
            "date": date,
            "meeting_name" : meeting_name,
            "keywords":keywordDic,
            "summarizer":summaryDic,
            "file_url":URLDic,
            "audio_waveform":audioWaveform
        }

        return finalDic
