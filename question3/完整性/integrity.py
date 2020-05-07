# 计算答复意见完整性
import jieba
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from question3.完整性.get_head_tail_frequently_word import get_frequency

outpath = '../data/完整性.xls'
data = pd.read_excel('../data/附件4_清洗后.xlsx')
reply = data['答复意见']


def data_jieba(message_list):
    jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/places.txt')
    jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/changsha_transportation_ns.txt')
    jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/changsha_houses_ns.txt')
    jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/changsha_area_ns.txt')

    data_cut = pd.Series(message_list).apply(lambda x: jieba.lcut(x))
    # 去除停用词 csv 默认 ,作为分隔符 用sep取一个数据里不存在的字符作为分隔符保障顺利读取
    stop_words = pd.read_csv('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/stopword.txt',
                             sep='hhhh',
                             encoding='GB18030', engine='python')
    # pd转列表拼接  iloc[:,0] 取第0列
    stop_words = list(stop_words.iloc[:, 0]) + [' ', '...', '', '  ', '→', '-', '：', ' ●', '\t', '\n', '！', '？']
    data_after_stop = data_cut.apply(lambda x: [i.strip() for i in x if i not in stop_words])

    data_after_jieba = []
    for temp_theme in data_after_stop:
        # keywords = " ".join(temp_theme)
        # data_after_jieba.append(keywords)
        # for i in temp_theme:
        data_after_jieba.append(temp_theme)
    return data_after_jieba


word_frequency = get_frequency()
word_frequency_key = list(word_frequency.keys())
reply_jieba = data_jieba(reply)
# 计算完整性
score = []
for temp_reply in reply_jieba:
    temp_score = 0
    for i in temp_reply:
        if word_frequency_key.__contains__(i):
            temp_score += word_frequency.get(i)
    score.append(temp_score)

# 归一化

# 将数据集进行归一化处理
my_matrix = np.array(score)
scaler = MinMaxScaler(feature_range=(0, 1))
scaler.fit_transform(my_matrix.reshape(-1, 1))
my_matrix_normorlize = scaler.transform(my_matrix.reshape(-1, 1))
temp_score_list = my_matrix_normorlize.tolist()
score_list = []
for i in temp_score_list:
    score_list.append(i[0])


# 划分标准
def get_evaluate(temp_num):
    if temp_num < 0.1:
        return 'E'
    elif temp_num < 0.2:
        return 'D'
    elif temp_num < 0.55:
        return 'C'
    elif temp_num < 0.8:
        return 'B'
    elif temp_num < 0.9:
        return 'A'
    else:
        return 'A+'


evaluate = []
for i in score_list:
    evaluate.append(get_evaluate(i))

# 写入数据
data['完整性'] = score
data['完整性归一化'] = score_list
data['完整性评价'] = evaluate
data.to_excel(outpath, index=None)
