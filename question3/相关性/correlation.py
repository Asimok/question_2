import jieba
import pandas as pd

from question2.数据清洗.date_format import get_date_interval
from question2.数据清洗.sentence_similarity import tf_similarity

outpath = '../data/相关性_回复间隔.xls'

data = pd.read_excel('/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/data/附件4_清洗后.xlsx')
message_detail = data['留言详情']
reply = data['答复意见']
# reply.apply(lambda x: str(x).replace(head, ''))
message_time = list(data['留言时间'])
reply_time = list(data['答复时间'])

# 答复时间间隔
interval = []
for i in range(len(reply)):
    temp_interval = get_date_interval(message_time[i], reply_time[i])
    interval.append(temp_interval)
# 未分词的相关性
similarity = []
for i in range(len(reply)):
    temp_similarity = tf_similarity(message_detail[i], reply[i])
    similarity.append(temp_similarity)
similarity.index(0)
pd.Series(similarity).max()
pd.Series(interval).median()
# 分词后的相关性

temp_message_detail = []
temp_reply = []
for index in message_detail:
    temp_message_detail.append(index)
for index in reply:
    temp_reply.append(index)
"""
l:习用语 nr:人名 nz:其他专名 ns:地名
"""
jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/places.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/changsha_transportation_ns.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/changsha_houses_ns.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/changsha_area_ns.txt')


def data_jieba(message_list):
    data_cut = pd.Series(message_list).apply(lambda x: jieba.lcut(x))
    # 去除停用词 csv 默认 ,作为分隔符 用sep取一个数据里不存在的字符作为分隔符保障顺利读取
    stop_words = pd.read_csv('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/stopword.txt', sep='hhhh',
                             encoding='GB18030', engine='python')
    # pd转列表拼接  iloc[:,0] 取第0列
    stop_words = list(stop_words.iloc[:, 0]) + [' ', '...', '', '  ', '→', '-', '：', ' ●', '\t', '\n', '！', '？']
    data_after_stop = data_cut.apply(lambda x: [i.strip() for i in x if i not in stop_words])

    data_after_jieba = []
    for temp_theme in data_after_stop:
        keywords = " ".join(temp_theme)
        data_after_jieba.append(keywords)
    return data_after_jieba


message_detail_jieba = data_jieba(temp_message_detail)
reply_jieba = data_jieba(temp_reply)
similarity_jieba = []
for i in range(len(reply_jieba)):
    temp_similarity = tf_similarity(message_detail_jieba[i], reply_jieba[i])
    similarity_jieba.append(temp_similarity)

pd.Series(similarity_jieba).max()
# 写入数据
data['相关性'] = similarity
data['分词后相关性'] = similarity_jieba
data['回复间隔'] = interval

data.to_excel(outpath)
print('导出', outpath)
