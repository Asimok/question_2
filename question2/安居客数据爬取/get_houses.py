"""
爬取安居客(https://cs.fang.anjuke.com) 长沙市所有楼盘名
生成自定义jieba分词词典
输出文件：
changsha_houses_ns.txt
"""
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
houses_url = 'https://cs.fang.anjuke.com/loupan/?pi=baidu-cpcaf-cs-ty1&kwid=16557240308&bd_vid=10525884175306697072'
driver.get(houses_url)
html = driver.page_source
dom = etree.HTML(html, etree.HTMLParser(encoding='utf-8'))
data = []
wait = WebDriverWait(driver, 10)  # 等待10秒
i = 0
while i < 100:
    # 等待条件满足之后才进行下一步操作
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR,
         '#container > div.list-contents.theme-ajk-listcont > div.list-results > div.key-sort > div.sort-condi > span '
         '> em')))
    html = driver.page_source
    dom = etree.HTML(html, etree.HTMLParser(encoding='utf-8'))
    houses = dom.xpath(
        '//*[@id="container"]/div[2]/div[1]/div[@class="key-list imglazyload"]/div/div/a[1]/span/text()')
    for j in houses:
        data.append(j)
    condition = driver.find_element_by_css_selector(
        '#container > div.list-contents.theme-ajk-listcont > div.list-results > div.list-page > div > '
        'a.next-page.next-link')  # 寻找下一页按钮
    if not condition:
        break  # 已经到达最后一页
    confrim_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                         '#container > div.list-contents.theme-ajk-listcont > '
                                                         'div.list-results > div.list-page > div > '
                                                         'a.next-page.next-link')))
    confrim_btn.click()  # 翻页
    i += 1

with open('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/changsha_houses_ns.txt', 'w') as f:
    for i in data:
        f.write(i)
        f.write(' ')
        f.write('ns')
        f.write('\n')
