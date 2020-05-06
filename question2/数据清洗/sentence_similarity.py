import numpy as np
from scipy.linalg import norm
from sklearn.feature_extraction.text import CountVectorizer


# 计算句子相似度
def tf_similarity(s1, s2):
    def add_space(s):
        return ' '.join(list(s))

    # 将字中间加入空格
    s1, s2 = add_space(s1), add_space(s2)
    # 转化为TF矩阵
    cv = CountVectorizer(tokenizer=lambda s: s.split())
    corpus = [s1, s2]
    vectors = cv.fit_transform(corpus).toarray()
    # 计算TF系数
    return np.dot(vectors[0], vectors[1]) / (norm(vectors[0]) * norm(vectors[1]))

#
# sentence1 = "A市 经济 学院 强制 学生 实习"
# sentence2 = "A市 经济 学院 体育 学院 变相 强制 实习"
# print(tf_similarity(sentence1, sentence2))
