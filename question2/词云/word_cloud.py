"""
绘制留言主题的词云图
输入文件：
附件3_清洗后.xlsx
输出文件：
留言主题词云.png
"""
import jieba
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

data = pd.read_excel('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/附件3_清洗后.xlsx')
theme = data['留言主题']

# 分词
jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/places.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/changsha_transportation_ns.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/changsha_houses_ns.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/changsha_area_ns.txt')
data_cut = theme.apply(jieba.lcut)
# 去除停用词
stopWord = pd.read_csv('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/stopword.txt', sep='hhhh',
                       encoding='GB18030', engine='python')
stopWords = list(stopWord.iloc[:, 0]) + [' ']
data_after_stopWords = data_cut.apply(lambda x: [i for i in x if i not in stopWords])
# 去除空行
index = data_after_stopWords.apply(lambda x: len(x) != 0)
data_after_stopWords_mot_null = data_after_stopWords[index]
# 统计词频
dic = {}
for i in data_after_stopWords_mot_null:
    for j in i:
        if j not in dic.keys():
            dic[j] = 1
        else:
            dic[j] += 1
# dic.pop(' ')

mask = plt.imread('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/duihuakuan.jpg')
wc = WordCloud(font_path='/usr/share/fonts/opentype/noto/NotoSerifCJK-Medium.ttc', mask=mask, background_color='white')
wc.fit_words(dic)
plt.imshow(wc)
plt.axis('off')
plt.savefig('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/留言主题词云.png', dpi=400, bbox_inches='tight')
plt.show()
