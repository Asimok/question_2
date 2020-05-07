"""
爬取图吧(https://poi.mapbar.com)长沙市乡镇、街道、社区、小区、地铁站、公交站、道路等交通设施名
生成自定义jieba分词词典
输出文件：
changsha_transportation_ns.txt
"""
from lxml import etree
from selenium import webdriver

driver = webdriver.Chrome()
data = []


def get_data(codes):
    url = 'https://poi.mapbar.com/changsha/' + codes + '/'
    driver.get(url)
    html = driver.page_source
    dom = etree.HTML(html, etree.HTMLParser(encoding='utf-8'))
    temp_data = dom.xpath('//div[@class="sortC"]/dl/dd/a/text()')
    for i in temp_data:
        data.append(i)


data_list = ['G11', 'G12', 'G14', 'G15', 'G20', 'G21', 'G30', 'G31', 'G40', 'G50', 'G51', 'G60', 'G70', 'G80', 'G90',
             'GA0', 'GA2', 'GF0']
for index in data_list:
    get_data(index)

with open('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/changsha_transportation_ns.txt', 'w') as f:
    for i in data:
        f.write(i)
        f.write(' ')
        f.write('ns')
        f.write('\n')
