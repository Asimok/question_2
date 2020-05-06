import jieba.analyse
import pandas as pd
import numpy as np
import jieba.analyse
import jieba.posseg as psg
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import DBSCAN

from question2.数据清洗.date_format import get_date_interval

# path = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/数据清洗/示例数据_去除30天内同一用户相似度0.75+的留言.xls'
path = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/数据清洗/去除30天内同一用户相似度0.75+的留言.xls'
pos_com = pd.read_excel(path)
all_data = pd.read_excel(path)
predict_data = []
stop_words = pd.read_csv('../data/stopwords.txt', sep='hhhh', encoding='gb18030', engine='python')
# pd转列表拼接  iloc[:,0] 取第0列
stop_words = list(stop_words.iloc[:, 0]) + [' ', '...', '', '  ', '→', '-', '：', ' ●', '\t', '\n', '？', '，']
for index in pos_com['留言主题'].iloc[0:10]:
    predict_data.append(
        str(index).strip().replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '').replace('\u3000',
                                                                                                          '').replace(
            '*',
            '').replace(
            '\xa0', ''))
word2flagdict = {}
data_after_stop_without_jieba = []
for temp_theme in predict_data:
    data_cut = psg.cut(temp_theme)
    data_after_stop = []
    for i in data_cut:
        if i.word not in stop_words:
            if i.word != "":
                data_after_stop.append(i.word)
                word2flagdict[i.word] = i.flag
    keywords = " ".join(data_after_stop)
    data_after_stop_without_jieba.append(keywords)
"""
l:习用语 nr:人名 nz:其他专名 ns:地名
"""
jieba.load_userdict('../data/new_places.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/图吧数据爬取/changsha_transportation_ns.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/安居客数据爬取/changsha_houses_ns.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/安居客数据爬取/changsha_area_ns.txt')

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
data1 = pos_com['留言主题'].iloc[0:10]
d2 = pd.DataFrame({'留言主题': data1, '使用自定义词典分词': data_after_jieba, '未使用自定义词典分词': data_after_stop_without_jieba},
                  columns=['留言主题', '未使用自定义词典分词', '使用自定义词典分词'])
d2.to_excel('./留言主题分词展示.xlsx', index=None)
