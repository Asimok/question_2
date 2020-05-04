import jieba.analyse
import pandas as pd

path = '/home/asimov/PycharmProjects/question_2/question2/聚类分析/聚类结果明细表.xls'
data = pd.read_excel(path)
jieba.load_userdict('../data/new_places.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/question_2/question2/图吧数据爬取/changsha_transportation_ns.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/question_2/question2/安居客数据爬取/changsha_houses_ns.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/question_2/question2/安居客数据爬取/changsha_area_ns.txt')

info = ''
for i in range(len(data['留言详情'])):
    if list(data['问题ID'])[i] == 9:
        info += str(data['留言主题'][i]).strip()


def generate_people_and_loc(temp_set):
    PEOPLE_AND_LOC = []
    for temp_theme in temp_set['留言主题']:
        keywords = " ".join(
            jieba.analyse.extract_tags(sentence=temp_theme, topK=4, withWeight=False,
                                       allowPOS=(['ns'])))
        PEOPLE_AND_LOC.append(keywords)
    temp_id = temp_set['留言编号']
    temp_user = temp_set['留言用户']
    temp_time = temp_set['留言时间']
    temp_theme = temp_set['留言主题']
    temp_detail = temp_set['留言详情']
    col = ['留言编号', '留言用户', '留言时间', '地点/人群', '留言主题', '留言详情']
    temp_save = pd.DataFrame(
        {'留言编号': temp_id, '留言用户': temp_user, '留言时间': temp_time, '地点/人群': PEOPLE_AND_LOC, '留言主题': temp_theme,
         '留言详情': temp_detail},
        columns=col)
    temp_save.to_excel('./示例数据——地点_人群.xls', index=None)


# generate_people_and_loc(data)
"""
l:习用语 nr:人名 nz:其他专名 ns:地名
"""
a =jieba.analyse.extract_tags(sentence=info, topK=4, withWeight=False,
                           allowPOS=(['ns']))
print(a)