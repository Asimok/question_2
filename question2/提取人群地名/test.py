import jieba
from jieba import analyse

jieba.load_userdict('../data/new_places.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/question_2/question2/图吧数据爬取/changsha_transportation_ns.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/question_2/question2/安居客数据爬取/changsha_houses_ns.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/question_2/question2/安居客数据爬取/changsha_area_ns.txt')


def textrank_extract(text, keyword_num=10):
    textrank = analyse.textrank
    # analyse.set_stop_words('/home/asimov/PycharmProjects/question_2/question2/data/stopword.txt',encoding='gb18030')
    keywords = textrank(text, keyword_num)
    # 输出抽取出的关键词
    for keyword in keywords:
        print(keyword + "/ ", end='')
    print()


def tfidf_extract(text, keyword_num=10):
    tfidf = analyse.extract_tags
    # analyse.set_stop_words('/home/asimov/PycharmProjects/question_2/question2/data/stopword.txt')
    keywords = tfidf(text, keyword_num)
    # 输出抽取出的关键词
    for keyword in keywords:
        print(keyword + "/ ", end='')
    print()


# text = '6月19日,《2012年度“中国爱心城市”公益活动新闻发布会》在京举行。' + \
#        '中华社会救助基金会理事长许嘉璐到会讲话。基金会高级顾问朱发忠,全国老龄' + \
#        '办副主任朱勇,民政部社会救助司助理巡视员周萍,中华社会救助基金会副理事长耿志远,' + \
#        '重庆市民政局巡视员谭明政。晋江市人大常委会主任陈健倩,以及10余个省、市、自治区民政局' + \
#        '领导及四十多家媒体参加了发布会。中华社会救助基金会秘书长时正新介绍本年度“中国爱心城' + \
#        '市”公益活动将以“爱心城市宣传、孤老关爱救助项目及第二届中国爱心城市大会”为主要内容,重庆市' + \
#        '、呼和浩特市、长沙市、太原市、蚌埠市、南昌市、汕头市、沧州市、晋江市及遵化市将会积极参加' + \
#        '这一公益活动。中国雅虎副总编张银生和凤凰网城市频道总监赵耀分别以各自媒体优势介绍了活动' + \
#        '的宣传方案。会上,中华社会救助基金会与“第二届中国爱心城市大会”承办方晋江市签约,许嘉璐理' + \
#        '事长接受晋江市参与“百万孤老关爱行动”向国家重点扶贫地区捐赠的价值400万元的款物。晋江市人大' + \
#        '常委会主任陈健倩介绍了大会的筹备情况。'
text = '请问领导，政府对于A3区西湖街道茶场村五组是如何规划的？？？周边都拆迁了，为何只剩下我们这一小块块地方？？请问何时能启动拆迁？？请问领导，A市A3区西湖街道茶场村五组何时能启动拆迁？？既然在三年前就被A3区山国家大学科技城报批了用地红线手续，那三年过去了，何时才能启动拆迁？胡书记，您好！我是西湖街道茶场村五组的村民！请问政府，我们这里是如何规划的？？我们剩下的这些村民该何去何从？？？？期盼政府的回应！！！第一，请问胡书记，人民路过江隧道何时修？第二，请问，我们A3区西湖街道茶场村五组的村民何去何从？因为前年西二环拓改，修白云路，我们村五组拆迁了一小部分房屋。现在因为A3区山西大门的建设，我们村的六组全组需要拆迁……而现在却又剩下我们五组一小小部分村民居住在这里，我们该何去何从？我们也希望早日奔上小康生活！请政府不要把我们遗忘了！谢谢。'
print('TF-IDF模型结果：')
tfidf_extract(text)
print('TextRank模型结果：')
textrank_extract(text)
jieba.analyse.extract_tags(sentence=text, topK=4, withWeight=False,
                           allowPOS=(['ns','n']))
# TF - IDF模型结果：
# 晋江市 / 救助 / 爱心 / 基金会 / 公益活动 / 城市 / 中华 / 许嘉璐 / 陈健倩 / 孤老 /
# TextRank模型结果：
# 城市 / 爱心 / 救助 / 中国 / 社会 / 晋江市 / 基金会 / 大会 / 介绍 / 公益活动 /
