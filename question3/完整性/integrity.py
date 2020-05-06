# 计算答复意见完整性
import jieba
import pandas as pd

from question3.完整性.get_head_tail_frequently_word import get_frequency

data = pd.read_excel('../data/附件4_清洗后.xlsx')
reply = data['答复意见']


def data_jieba(message_list):
    jieba.load_userdict('../data/places.txt')
    jieba.load_userdict(
        '../图吧数据爬取/changsha_transportation_ns.txt')
    jieba.load_userdict('../安居客数据爬取/changsha_houses_ns.txt')
    jieba.load_userdict('../安居客数据爬取/changsha_area_ns.txt')

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
data['完整性'] = score
data.to_excel('../data/回复完整性.xls')
