# coding:utf-8
import math
import jieba.analyse
from collections import Counter

sentence1 = "A市经济学院强制学生实习"
sentence2 = "A市经济学院体育学院变相强制实习"


def anlyse_count(sentence):
    words = jieba.cut(sentence)
    words = [each.strip() for each in words]
    counter = Counter(words)
    for a in counter.most_common(20):
        print('%-10s\t%d' % (a[0], a[1]))
    print('\n')


# 关键词提取

jieba.load_userdict('./data/new_places.txt')
jieba.load_userdict('./data/new_places_country.txt')


def print_topic(text):
    tags = jieba.analyse.extract_tags(text, withWeight=True)
    print("%10s\t%s" % ('关键词', '权重'))
    for v, n in tags:
        print("%-10s\t%d" % (v, n * 10000))
    print('')


# 相似度判断
def cut_word(sentence):
    # 使用TF-IDF算法
    res = jieba.analyse.extract_tags(sentence=sentence, topK=20, withWeight=True)
    return res


def tf_idf(res1=None, res2=None):
    # 向量，可以用list表示
    vector_1 = []
    vector_2 = []
    # 词频，可以使用dict表示
    tf_1 = {i[0]: i[1] for i in res1}
    tf_2 = {i[0]: i[1] for i in res2}
    res = set(list(tf_1.keys()) + list(tf_2.keys()))

    # 填充词频向量
    for word in res:
        if word in tf_1:
            vector_1.append(tf_1[word])
        else:
            vector_1.append(0)
            if word in tf_2:
                vector_2.append(tf_2[word])
            else:
                vector_2.append(0)

    return vector_1, vector_2


def numerator(vector1, vector2):
    # 分子
    return sum(a * b for a, b in zip(vector1, vector2))


def denominator(vector):
    # 分母
    return math.sqrt(sum(a * b for a, b in zip(vector, vector)))


def run(vector1, vector2):
    return numerator(vector1, vector2) / (denominator(vector1) * denominator(vector2))


def get_similarity(text1, text2):
    vectors = tf_idf(res1=cut_word(sentence=text1), res2=cut_word(sentence=text2))
    # 相似度
    similarity = run(vector1=vectors[0], vector2=vectors[1])
    # 使用arccos计算弧度
    # rad = math.acos(similarity)
    return similarity


# anlyse_count(sentence)
# print_topic(sentence)


print(get_similarity(sentence2, sentence1))
