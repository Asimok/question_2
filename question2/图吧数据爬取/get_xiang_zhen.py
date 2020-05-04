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
html = driver.page_source
dom = etree.HTML(html, etree.HTMLParser(encoding='utf-8'))
xiaoqu = dom.xpath('//div[@class="sortC"]/dl/dd/a/text()')


url_road = 'https://poi.mapbar.com/changsha/G70/'
driver.get(url_road)
html = driver.page_source
dom = etree.HTML(html, etree.HTMLParser(encoding='utf-8'))
road = dom.xpath('//div[@class="sortC"]/dl/dd/a/text()')

url_subway = 'https://poi.mapbar.com/changsha/G11/'
driver.get(url_subway)
html = driver.page_source
dom = etree.HTML(html, etree.HTMLParser(encoding='utf-8'))
subway = dom.xpath('//div[@class="sortC"]/dl/dd/a/text()')

url_subway2 = 'https://poi.mapbar.com/changsha/G15/'
driver.get(url_subway2)
html = driver.page_source
dom = etree.HTML(html, etree.HTMLParser(encoding='utf-8'))
subway2 = dom.xpath('//div[@class="sortC"]/dl/dd/a/text()')

url_bus = 'https://poi.mapbar.com/changsha/G12/'
driver.get(url_bus)
html = driver.page_source
dom = etree.HTML(html, etree.HTMLParser(encoding='utf-8'))
bus = dom.xpath('//div[@class="sortC"]/dl/dd/a/text()')

url_train = 'https://poi.mapbar.com/changsha/G14/'
driver.get(url_train)
html = driver.page_source
dom = etree.HTML(html, etree.HTMLParser(encoding='utf-8'))
train = dom.xpath('//div[@class="sortC"]/dl/dd/a/text()')

with open('./changsha_ns.txt', 'w') as f:
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
    for i in road:
        f.write(i)
        f.write(' ')
        f.write('ns')
        f.write('\n')
with open('./changsha_traffic_ns.txt', 'w') as f:
    for i in bus:
        f.write(i)
        f.write(' ')
        f.write('ns')
        f.write('\n')
    for i in subway:
        f.write(i)
        f.write(' ')
        f.write('ns')
        f.write('\n')
    for i in subway2:
        f.write(i)
        f.write(' ')
        f.write('ns')
        f.write('\n')
    for i in train:
        f.write(i)
        f.write(' ')
        f.write('ns')
        f.write('\n')

# dict_zhen = {}
# len_zhen = len(zhen)
# len_xiaoqu = len(xiaoqu)
# for i in range(len(zhen)):
#     dict_zhen[zhen[i]] = i
#
# for i in range(len(xiaoqu)):
#     dict_zhen[xiaoqu[i]] = i + len_zhen
# data = pd.read_csv('/home/asimov/PycharmProjects/question_2/question2/data/places.txt', sep='hhh', engine='python',
#                    header=None)
# city = list(data[0])
# for i in range(len(city)):
#     dict_zhen[city[i]] = i + len_zhen + len_xiaoqu
# f1 = open('/home/asimov/PycharmProjects/Chinese-Text-Classification-Pytorch/THUCNews/data/vocab.pkl', 'rb')
# with open('/home/asimov/PycharmProjects/Chinese-Text-Classification-Pytorch/THUCNews/data/changsha_ns.pkl', 'wb',
#           ) as f:
#     pickle.dump(dict_zhen, f, )
#
# dat = pickle.load(f1)
