"""
参考： https://blog.csdn.net/Yellow_python/article/details/81021142
"""
from typing import Optional

from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.similarities import SparseMatrixSimilarity
from jieba import lcut
from sqlalchemy.engine import Row


class RecommendedNews:
    """
    通过相似度推荐 新闻
    """

    def __init__(self):
        self.news_words: Optional[list[list]] = None
        self.key_word: Optional[list] = None

    def set_news_words(self, news_words: list[list]) -> None:
        self.news_words = news_words

    def set_key_words(self, key_words: list) -> None:
        self.key_word = lcut(" ".join([key_word for key_word in key_words]))

    @staticmethod
    def cut(news: list[Row]) -> list:
        """ 分词
        """
        return [[_news.news_id, lcut(_news.content)] for _news in news]

    def top_ten_new_ids(self) -> list[str]:
        """ 得到相似度分数前十新闻
        """
        texts = [_news[1] for _news in self.news_words]
        # 基于文本集建立词典
        dictionary = Dictionary(texts)
        # 并获得词典特征数
        num_features = len(dictionary.token2id)

        # 基于词典，将【分词列表集】转换成【稀疏向量集】，称作【语料库】
        news_corpus = [dictionary.doc2bow(text) for text in texts]
        # 基于词典，将【搜索词】也转换为【稀疏向量】
        kwy_word_vector = dictionary.doc2bow(self.key_word)

        # 创建 TF-IDF模型，传入新闻文本语料库来训练
        tfidf_model = TfidfModel(news_corpus)
        # 用训练好的【TF-IDF模型】处理【被检索文本】和【搜索词】
        tf_news = tfidf_model[news_corpus]  # 此处将【语料库】用作【被检索文本】
        tf_kwy_word = tfidf_model[kwy_word_vector]

        # 相似度计算
        sparse_matrix = SparseMatrixSimilarity(tf_news, num_features)
        similarities = sparse_matrix.get_similarities(tf_kwy_word)

        results = {}
        for index, similarity in enumerate(similarities):
            results[self.news_words[index][0]] = similarity

        # 按相似度降序
        results = sorted(results.items(), key=lambda d: d[1], reverse=True)
        # 取前十
        return [_line[0] for _line in results][0:10]
