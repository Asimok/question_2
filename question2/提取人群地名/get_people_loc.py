import jieba.analyse
import pandas as pd

path = '/home/asimov/PycharmProjects/question_2/question2/聚类分析/示例数据_聚类_主题_去重_热度_0.9_4.xls'
data = pd.read_excel(path)


def generate_people_and_loc(temp_set):
    PEOPLE_AND_LOC = []
    for temp_theme in temp_set['留言主题']:
        keywords = " ".join(
            jieba.analyse.extract_tags(sentence=temp_theme, topK=4, withWeight=False,
                                       allowPOS=(['n', 'ns', 'l', 'nr', 'nz'])))
        PEOPLE_AND_LOC.append(keywords)
    temp_id = temp_set['留言编号']
    temp_user = temp_set['留言用户']
    temp_time = temp_set['留言时间']
    temp_theme = temp_set['留言主题']
    col = ['留言编号', '留言用户', '留言时间', '地点/人群', '留言主题']
    temp_save = pd.DataFrame(
        {'留言编号': temp_id, '留言用户': temp_user, '留言时间': temp_time, '地点/人群': PEOPLE_AND_LOC, '留言主题': temp_theme},
        columns=col)
    temp_save.to_excel('./示例数据——地点_人群.xls', index=None)


generate_people_and_loc(data)
