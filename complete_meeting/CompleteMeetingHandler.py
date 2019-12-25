from entity_recognisation.tasks.entity_recognisation_tasks import entityRecog

class CompleteMeetingHandler:
    def meetingHandler(self, meetingid):
        entityRecog.delay(meetingId = meetingid)
