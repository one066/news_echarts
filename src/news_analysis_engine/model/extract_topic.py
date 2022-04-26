from textrank4zh import TextRank4Keyword, TextRank4Sentence


class ExtractTopic:
    """
    主题提取
    """

    @staticmethod
    def text_rank(content: str) -> list:
        """
        text 算法提取关键字、关键词
        """
        text_rank4_keyword = TextRank4Keyword()
        text_rank4_keyword.analyze(text=content, lower=True, window=2)

        text_rank4_sentence = TextRank4Sentence()
        text_rank4_sentence.analyze(
            text=content, lower=True, source='all_filters'
        )

        keywords = [
            item.word
            for item in text_rank4_keyword.get_keywords(8, word_min_len=1)
        ]
        sentences = [
            item.sentence
            for item in text_rank4_sentence.get_key_sentences(num=1)
        ]
        return [keywords, sentences]
