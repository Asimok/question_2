"""
计算答复意见完整性
输入文件：
附件4_清洗后.xlsx
输出文件：
完整性.xls
"""
import re

import jieba
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from question3.完整性.get_head_tail_frequently_word import get_frequency
from question3.相关性.get_head_tail import get_head_tail

outpath = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/data/完整性.xls'
data = pd.read_excel('/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/data/附件4_清洗后.xlsx')
read_reply = data['答复意见']
data_contain_nt = data['是否包含机构']
reply = []
# 去除标准开头结尾
for i in read_reply:
    head, tail = get_head_tail(i)
    temp_str = str(i).replace(head, '')
    temp_str = temp_str.replace(tail, '')
    reply.append(temp_str)


def data_jieba(message_list):
    jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/places.txt')
    jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/changsha_transportation_ns.txt')
    jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/changsha_houses_ns.txt')
    jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/changsha_area_ns.txt')

    data_cut = pd.Series(message_list).apply(lambda x: jieba.lcut(x))
    stop_words = pd.read_csv('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/stopword.txt',
                             sep='hhhh',
                             encoding='GB18030', engine='python')
    stop_words = list(stop_words.iloc[:, 0]) + [' ', '...', '', '  ', '→', '-', '：', ' ●', '\t', '\n', '！', '？']
    data_after_stop = data_cut.apply(lambda x: [i.strip() for i in x if i not in stop_words])

    data_after_jieba = []
    for temp_theme in data_after_stop:
        data_after_jieba.append(temp_theme)
    return data_after_jieba


word_frequency = get_frequency()
word_frequency_key = list(word_frequency.keys())
reply_jieba = data_jieba(reply)
# 计算完整性
score = []
# 标准开头结尾完整性
for temp_reply in reply_jieba:
    temp_score = 0
    for i in temp_reply:
        if word_frequency_key.__contains__(i):
            temp_score += word_frequency.get(i)
    score.append(temp_score)


# 法律法规完整性
def contain_law(string):
    p1 = re.compile(r'[《](.*?)[》]', re.S)  # 最小匹配
    temp_ans_list = []
    for temp_law_id in re.findall(p1, string):
        temp_ans_list.append(str(temp_law_id))
    if len(temp_ans_list) > 0:
        return True
    else:
        return False


for i in range(len(reply)):
    if contain_law(reply[i]):
        score[i] += 1

# 机构完整性

for temp_str_id in range(len(reply)):
    if bool(data_contain_nt[temp_str_id]):
        score[temp_str_id] += 1

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
    if temp_num < 0.05:
        return 'E'
    elif temp_num < 0.2:
        return 'D'
    elif temp_num < 0.5:
        return 'C'
    elif temp_num < 0.8:
        return 'B'
    elif temp_num < 0.95:
        return 'A'
    else:
        return 'A+'


evaluate = []
for i in score_list:
    evaluate.append(get_evaluate(i))

# 写入数据

write_data = pd.DataFrame({'留言编号': data['留言编号'], '完整性指数': score_list, '完整性评价': evaluate, },
                          columns=['留言编号', '完整性指数', '完整性评价'])
write_data.to_excel(outpath, index=None)
print('导出', outpath)
