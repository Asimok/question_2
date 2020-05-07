"""
爬取安居客(https://cs.fang.anjuke.com) 长沙市所有小区名
生成自定义jieba分词词典
输出文件：
changsha_area_ns.txt
"""
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
area_url = 'https://cs.anjuke.com/community/?from=navigation'
driver.get(area_url)
html = driver.page_source
dom = etree.HTML(html, etree.HTMLParser(encoding='utf-8'))
data = []

wait = WebDriverWait(driver, 10)  # 等待10秒
i = 0
while i < 100:
    # 等待条件满足之后才进行下一步操作
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR,
         '#list-content > div.sortby > span > em:nth-child(2)')))
    html = driver.page_source
    dom = etree.HTML(html, etree.HTMLParser(encoding='utf-8'))
    area = dom.xpath(
        '//*[@id="list-content"]/div/div[1]/h3/a/@title')
    for j in area:
        data.append(j)
    condition = driver.find_element_by_css_selector(
        'body > div.w1180 > div.maincontent > div.page-content > div > a.aNxt')  # 寻找下一页按钮
    if not condition:
        break  # 已经到达最后一页
    confrim_btn = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'body > div.w1180 > div.maincontent > div.page-content > div > a.aNxt')))
    confrim_btn.click()  # 翻页
    i += 1

with open('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/changsha_area_ns.txt', 'w') as f:
    for i in data:
        f.write(i)
        f.write(' ')
        f.write('ns')
        f.write('\n')
