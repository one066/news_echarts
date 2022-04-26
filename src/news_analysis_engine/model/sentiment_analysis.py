from snownlp import SnowNLP


class SentimentAnalysis:
    """
    文章情感分析
    """

    POSITIVE = "积极"
    NEGATIVE = "消极"
    NEUTRAL = "中性"

    def get_sentiment(self, content: str) -> str:
        try:
            positive_score = SnowNLP(content).sentiments
        except ZeroDivisionError:
            return self.NEUTRAL

        if positive_score < 0.35:
            return self.NEGATIVE

        if 0.65 < positive_score:
            return self.POSITIVE

        return self.NEUTRAL
