# import copy
#
# import jieba
# import numpy as np
# import scipy
# from sklearn.decomposition import LatentDirichletAllocation
# from sklearn.feature_extraction.text import TfidfVectorizer
#
#
# class ExtractTopicV1:
#     """
#     主题提取
#     """
#
#     def __init__(self):
#         self.words_bag = []
#
#     def set_news(self, news: list) -> None:
#         """构建词袋
#         """
#         self.words_bag = [
#             " ".join(jieba.lcut(a_news["content"])) for a_news in news
#         ]
#
#     def get_word_frequency_vector(self) -> tuple[scipy, list]:
#         """ tf-idf 词频向量
#         """
#         tf_idf_vector = TfidfVectorizer()
#         tf_vectorized = tf_idf_vector.fit_transform(copy.copy(self.words_bag))
#         tf_feature_names = tf_idf_vector.get_feature_names()
#         return tf_vectorized, tf_feature_names
#
#     def lda(self):
#         """ LDA 主题模型 提取主题
#         """
#         lda = LatentDirichletAllocation(
#             n_components=27,  # 主题个数
#             max_iter=50,  # EM算法的最大迭代次数
#             learning_method='online',
#             learning_offset=50.,  # 仅仅在算法使用online时有意义，取值要大于1。用来减小前面训练样本批次对最终模型的影响
#             random_state=0
#         )
#
#         tf_vectorized, tf_feature_names = self.get_word_frequency_vector()
#         _lda = lda.fit_transform(tf_vectorized)
#
#         lda_corpus = np.array(_lda)
#         lda_corpus_one = np.argmax(lda_corpus, axis=1)
#
#         kk = []
#         for topic_idx, topic in enumerate(lda.components_):
#             kk.append(
#                 " ".join([tf_feature_names[i] for i in topic.argsort()[:-3:-1]])
#             )
#
#         print(kk)
#         print(lda_corpus_one)
#
#         for index, i in enumerate(lda_corpus_one):
#             print(index, kk[i])
