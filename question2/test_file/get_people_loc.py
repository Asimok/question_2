import jieba.analyse
import pandas as pd

path = '//question2/聚类分析/聚类结果明细表.xls'
data = pd.read_excel(path)
jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/places.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/changsha_transportation_ns.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/changsha_houses_ns.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/changsha_area_ns.txt')

"""
l:习用语 nr:人名 nz:其他专名 ns:地名
"""
a = jieba.analyse.extract_tags(sentence=info, topK=4, withWeight=False,
                               allowPOS=(['ns']))
print(a)
