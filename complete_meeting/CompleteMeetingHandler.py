from entity_recognisation.tasks.entity_recognisation_tasks import entityRecog
from keyword_recognization.tasks.keyword_reconize_tasks import keywordRecog
from text_summarizer.tasks.text_summarizer_tasks import textSummarizer
from sentiment_analyzer.tasks.sentiment_analyzer_tasks import sentimentAnalyzer

class CompleteMeetingHandler:
    def meetingHandler(self, meetingid):
        entityRecog.delay(meetingId = meetingid)
        keywordRecog.delay(meetingId=meetingid)
        textSummarizer.delay(meetingId=meetingid)
        sentimentAnalyzer.delay(meetingId=meetingid)
