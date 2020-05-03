"""
分成7类 提取关键词
"""
import jieba.analyse
import jieba.posseg as psg
import pandas as pd

classification = ['城乡建设', '环境保护', '交通运输', '教育文体', '劳动和社会保障', '商贸旅游', '卫生计生']
path = '/home/asimov/文档/2020数据挖掘/C题/示例数据/附件3.xlsx'
data = pd.read_excel(path)

cxjs_data = data.loc[data['预测一级标签'] == classification[0]]
hjbh_data = data.loc[data['预测一级标签'] == classification[1]]
jtys_data = data.loc[data['预测一级标签'] == classification[2]]
jywt_data = data.loc[data['预测一级标签'] == classification[3]]
ldhshbz_data = data.loc[data['预测一级标签'] == classification[4]]
smly_data = data.loc[data['预测一级标签'] == classification[5]]
wsjs_data = data.loc[data['预测一级标签'] == classification[6]]

cxjs_data.to_excel('/home/asimov/PycharmProjects/question_2/question2/classifications_seven/cxjs_data.xls')
hjbh_data.to_excel('/home/asimov/PycharmProjects/question_2/question2/classifications_seven/hjbh_data.xls')
jtys_data.to_excel('/home/asimov/PycharmProjects/question_2/question2/classifications_seven/jtys_data.xls')
jywt_data.to_excel('/home/asimov/PycharmProjects/question_2/question2/classifications_seven/jywt_data.xls')
ldhshbz_data.to_excel('/home/asimov/PycharmProjects/question_2/question2/classifications_seven/ldhshbz_data.xls')
smly_data.to_excel('/home/asimov/PycharmProjects/question_2/question2/classifications_seven/smly_data.xls')
wsjs_data.to_excel('/home/asimov/PycharmProjects/question_2/question2/classifications_seven/wsjs_data.xls')
"""
l:习用语 nr:人名 nz:其他专名 ns:地名
"""
jieba.load_userdict('./data/new_places.txt')
jieba.load_userdict('./data/changsha_ns.txt')


# ----------------------------提取地名 人群--------------------------- #

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
    temp_disagree = temp_set['反对数']
    temp_agree = temp_set['点赞数']
    temp_label = list(temp_set['预测一级标签'])[0]
    col = ['留言编号', '留言用户', '留言时间', '地点/人群', '反对数', '点赞数']
    temp_save = pd.DataFrame(
        {'留言编号': temp_id, '留言用户': temp_user, '留言时间': temp_time, '地点/人群': PEOPLE_AND_LOC, '反对数': temp_disagree,
         '点赞数': temp_agree}, columns=col)
    temp_save.to_excel('./classifications_seven_PEOPLE_AND_LOC/' + temp_label + '——地点_人群_主题.xls', index=None)


generate_people_and_loc(cxjs_data)
generate_people_and_loc(hjbh_data)
generate_people_and_loc(jtys_data)
generate_people_and_loc(jywt_data)
generate_people_and_loc(ldhshbz_data)
generate_people_and_loc(smly_data)
generate_people_and_loc(wsjs_data)
