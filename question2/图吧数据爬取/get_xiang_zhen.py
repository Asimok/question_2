from lxml import etree
from selenium import webdriver
import pickle
import pandas as pd

driver = webdriver.Chrome()
url_zhen = 'https://poi.mapbar.com/changsha/FF0/'
driver.get(url_zhen)
html = driver.page_source
dom = etree.HTML(html, etree.HTMLParser(encoding='utf-8'))
zhen = dom.xpath('//div[@class="sortC"]/dl/dd/a/text()')

url_xiaoqu = 'https://poi.mapbar.com/changsha/F10/'
driver.get(url_xiaoqu)
html2 = driver.page_source
dom2 = etree.HTML(html2, etree.HTMLParser(encoding='utf-8'))
xiaoqu = dom2.xpath('//div[@class="sortC"]/dl/dd/a/text()')
xiaoqu.index('麓谷明珠小区')

with open('../data/changsha_ns.txt', 'w') as f:
    for i in zhen:
        f.write(i)
        f.write(' ')
        f.write('ns')
        f.write('\n')
    for i in xiaoqu:
        f.write(i)
        f.write(' ')
        f.write('ns')
        f.write('\n')
dict_zhen = {}
len_zhen = len(zhen)
len_xiaoqu = len(xiaoqu)
for i in range(len(zhen)):
    dict_zhen[zhen[i]] = i

for i in range(len(xiaoqu)):
    dict_zhen[xiaoqu[i]] = i + len_zhen
data = pd.read_csv('/home/asimov/PycharmProjects/question_2/question2/data/places.txt', sep='hhh', engine='python',
                   header=None)
city = list(data[0])
for i in range(len(city)):
    dict_zhen[city[i]] = i + len_zhen + len_xiaoqu
f1 = open('/home/asimov/PycharmProjects/Chinese-Text-Classification-Pytorch/THUCNews/data/vocab.pkl', 'rb')
with open('/home/asimov/PycharmProjects/Chinese-Text-Classification-Pytorch/THUCNews/data/changsha_ns.pkl', 'wb',
          ) as f:
    pickle.dump(dict_zhen, f, )

dat = pickle.load(f1)
