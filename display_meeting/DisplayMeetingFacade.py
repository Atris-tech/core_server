from start_meeting.models import CreateMeeting
from transcribe.models import Transcribe
from sound_classify.models import Classify
from entity_recognisation.models import Recognise
class DisplayMeetingFacade:
    def getData(meetingID):
        createMeetingObj = CreateMeeting.objects.get(meeting_id = meetingID)
        transcribeObj = Transcribe.objects.filter(meeting_id = createMeetingObj)
        classifyObj =  Classify.objects.filter(meeting_id = createMeetingObj)
        entityObj = Recognise.objects.get(meeting_id=createMeetingObj)
        entityDic = entityObj.entities
        transcribeDic = transcribeObj.order_by('segment_id').values()
        classifyDic = classifyObj.order_by('segment_id').values()
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
                "transcribe" : finalArray,
                "entities" : entityDic
            }
        return finalDic
