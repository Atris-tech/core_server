from start_meeting.models import CreateMeeting
from transcribe.models import Transcribe
from sound_classify.models import Classify

class DisplayMeetingFacade:
    def getData(meetingID):
        createMeetingObj = CreateMeeting.objects.get(meeting_id = meetingID)
        transcribeObj = Transcribe.objects.filter(meeting_id = createMeetingObj)
        classifyObj =  Classify.objects.filter(meeting_id = createMeetingObj)
        transcribeDic = transcribeObj.order_by('segment_id').values()
        classifyDic = classifyObj.order_by('segment_id').values()
        finalDic = {}
        count = 0
        for val1, val2 in zip(transcribeDic, classifyDic):
            newSegment = "Segment_" + str(count)
            finalDic.update(
                {
                    newSegment: {
                        "text": val1["text"],
                        "sound": val2["sounds"]
                    }
                }
            )
            count = count + 1
        return finalDic
