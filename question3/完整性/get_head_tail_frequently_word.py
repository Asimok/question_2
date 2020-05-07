"""
获取标准开头结尾高频词
输入文件：
附件4_清洗后.xlsx
输出文件：
开头结尾.xls
输出参数：
标准开头结尾词频
"""
import jieba
import pandas as pd


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
        for i in temp_theme:
            data_after_jieba.append(i)
    return data_after_jieba


def get_frequency():
    path = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/data/开头结尾.xls'
    data = pd.read_excel(path)
    head = data['开头']
    tail = data['结尾']
    head_sub = []
    tail_sub = []
    for i in head:
        if str(i) != 'nan':
            head_sub.append(i)
    for i in tail:
        if str(i) != 'nan':
            tail_sub.append(i)

    d1 = data_jieba(head_sub)
    d2 = data_jieba(tail_sub)
    d3 = pd.Series(d2 + d1)
    num_count = d3.count()
    word_frequency = dict(d3.value_counts())

    for keys in word_frequency.keys():
        word_frequency[keys] = word_frequency.get(keys) / num_count
    return word_frequency
