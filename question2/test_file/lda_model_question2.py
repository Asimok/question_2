import jieba.analyse
import pandas as pd
from gensim.corpora import Dictionary
from gensim.models import LdaModel

message_data = pd.read_excel('./classifications_seven/cxjs_data.xls')

predict_data = []

for index in message_data['留言详情']:
    predict_data.append(
        str(index).strip().replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '').replace('\u3000',
                                                                                                          '').replace(
            '*',
            '').replace(
            '\xa0', ''))
"""
l:习用语 nr:人名 nz:其他专名 ns:地名
"""
jieba.load_userdict('./data/places.txt')
jieba.load_userdict('./data/changsha_ns.txt')

data_cut = pd.Series(predict_data).apply(lambda x: jieba.lcut(x))
# 去除停用词 csv 默认 ,作为分隔符 用sep取一个数据里不存在的字符作为分隔符保障顺利读取
stop_words = pd.read_csv('../data/stopword.txt', sep='hhhh', encoding='GB18030', engine='python')
# pd转列表拼接  iloc[:,0] 取第0列
stop_words = list(stop_words.iloc[:, 0]) + [' ', '...', '', '  ', '→', '-', '：', ' ●', '\t', '\n']
data_after_stop = data_cut.apply(lambda x: [i.strip() for i in x if i not in stop_words])

PEOPLE_AND_LOC = []
for temp_theme in predict_data:
    # keywords = " ".join(
    #     jieba.analyse.extract_tags(sentence=temp_theme, topK=4, withWeight=False,
    #                                allowPOS=(['n', 'ns', 'l', 'nr', 'nz'])))
    # 去除停用词 csv 默认 ,作为分隔符 用sep取一个数据里不存在的字符作为分隔符保障顺利读取
    data_cut = jieba.lcut(temp_theme)
    stop_words = pd.read_csv('../data/stopword.txt', sep='hhhh', encoding='GB18030', engine='python')
    # pd转列表拼接  iloc[:,0] 取第0列
    stop_words = list(stop_words.iloc[:, 0]) + [' ', '...', '', '  ', '→', '-', '：', ' ●', '\t', '\n']

    data_after_stop = []
    for i in data_cut:
        if i not in stop_words:
            if i != "":
                data_after_stop.append(i)
    keywords = " ".join(data_after_stop)
    PEOPLE_AND_LOC.append(keywords)

# 地点/人群
# 去除空格
mid = list(pd.Series(PEOPLE_AND_LOC).str.split(' '))
dictionary = Dictionary(mid)
bow = [dictionary.doc2bow(com) for com in mid]
# 模型构建
pos_model = LdaModel(corpus=bow, id2word=dictionary, num_topics=3)
pos_model.get_term_topics(2)
print(pos_model.print_topic(0))
pos_model.print_topic(1)
pos_model.print_topic(2)
