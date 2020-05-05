import jieba.analyse
import pandas as pd
import numpy as np
import jieba.analyse
import jieba.posseg as psg
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import DBSCAN

from question2.数据清洗.date_format import get_date_interval

# path = '/home/asimov/PycharmProjects/question_2/question2/数据清洗/示例数据_去除30天内同一用户相似度0.75+的留言.xls'
path = '/home/asimov/PycharmProjects/question_2/question2/数据清洗/去除30天内同一用户相似度0.75+的留言.xls'
pos_com = pd.read_excel(path)
all_data = pd.read_excel(path)
predict_data = []

for index in pos_com['留言详情'].iloc[0:10]:
    predict_data.append(
        str(index).strip().replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '').replace('\u3000',
                                                                                                          '').replace(
            '*',
            '').replace(
            '\xa0', ''))
"""
l:习用语 nr:人名 nz:其他专名 ns:地名
"""
jieba.load_userdict('../data/new_places.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/question_2/question2/图吧数据爬取/changsha_transportation_ns.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/question_2/question2/安居客数据爬取/changsha_houses_ns.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/question_2/question2/安居客数据爬取/changsha_area_ns.txt')

data_cut = pd.Series(predict_data).apply(lambda x: jieba.lcut(x))
# 去除停用词 csv 默认 ,作为分隔符 用sep取一个数据里不存在的字符作为分隔符保障顺利读取
stop_words = pd.read_csv('../data/stopwords.txt', sep='hhhh',encoding='gb18030', engine='python')
# pd转列表拼接  iloc[:,0] 取第0列
stop_words = list(stop_words.iloc[:, 0]) + [' ', '...', '', '  ', '→', '-', '：', ' ●', '\t', '\n','？','，']
data_after_stop = data_cut.apply(lambda x: [i.strip() for i in x if i not in stop_words])

word2flagdict = {}
data_after_jieba = []
for temp_theme in predict_data:
    data_cut = psg.cut(temp_theme)
    data_after_stop = []
    for i in data_cut:
        if i.word not in stop_words:
            if i.word != "":
                data_after_stop.append(i.word)
                word2flagdict[i.word] = i.flag
    keywords = " ".join(data_after_stop)
    data_after_jieba.append(keywords)
# all_data['主题分词'] = data_after_jieba
data1 = pos_com['留言详情'].iloc[0:10]
d2 = pd.DataFrame({'留言详情': data1, '分词结果': data_after_jieba}, columns=['留言详情', '分词结果'])
d2.to_excel('./留言详情分词展示.xlsx', index=None)
