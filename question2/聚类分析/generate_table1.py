"""
生成 表1-热点问题表
输入文件：
聚类结果明细表.xls
输出文件：
问题描述.xls
地点人群.xls
热点问题表.xls
"""
import hanlp
import jieba.analyse
import pandas as pd
from textrank4zh import TextRank4Sentence

in_path = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/聚类结果明细表.xls'
out_path = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/问题描述.xls'
out_path2 = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/地点人群.xls'
out_path3 = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/answer2/热点问题表.xls'
df_in = pd.read_excel(in_path)
jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/places.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/changsha_transportation_ns.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/changsha_houses_ns.txt')
jieba.load_userdict('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/changsha_area_ns.txt')

# -------------------------------------生成 问题描述------------------------------------

df_hot_score = df_in['热度指数'].tolist()
hot_score = []
for i in df_hot_score:
    if not str(i).__eq__(' '):
        hot_score.append(i)
df_time_span = df_in['时间范围'].tolist()
time_span = []
for i in df_time_span:
    if not str(i).__eq__(' '):
        time_span.append(i)
abb = []
question_list = []
for i in list(df_in['问题ID']):
    if i != ' ':
        question_list.append(i)
for question_id in question_list[0:5]:
    question_id = int(question_id)
    df_in_id = df_in[df_in['问题ID'] == question_id]
    title = '\n'.join(df_in_id['留言主题'].tolist())
    sentence = TextRank4Sentence(delimiters='\n')
    sentence.analyze(text=title, lower=True)
    abstract = '\n'.join([item.sentence for item in sentence.get_key_sentences(num=1)])
    abb.append(abstract)
    print("主题句为：", abstract)
# print(abb)
df1 = pd.DataFrame({'问题ID': [i for i in range(1, 5 + 1)], '问题描述': abb})
df1.to_excel(out_path, index=None)
# -----------------------------------提取 地点人群------------------------------------
tokenizer = hanlp.load('PKU_NAME_MERGED_SIX_MONTHS_CONVSEG')
recognizer = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)
loc_people = []
for theme in abb:
    loc_people.append(recognizer.predict(list(theme)))
# print(loc_people)
str_loc_people = []
for i in range(len(loc_people)):
    temp_str = ''
    if len(list(loc_people[i])) == 0:
        temp_ns = jieba.analyse.extract_tags(sentence=abb[i], topK=4, withWeight=False,
                                             allowPOS=(['ns']))
        for m in temp_ns:
            temp_str += m
    else:
        for j in loc_people[i]:
            temp_str += j[0]
    str_loc_people.append(temp_str)
df2 = pd.DataFrame({'问题ID': question_list[0:5], '地点/人群': str_loc_people, '问题描述': abb},
                   columns=['问题ID', '地点/人群', '问题描述'])
df2.to_excel(out_path2, index=None)
print('导出文件: ', out_path2)
# -------------------------------生成 表1-热点问题表------------------------------
write_tb1_abb = abb[0:5]
write_tb1_hot_score = hot_score[0:5]
write_tb1_loc_people = str_loc_people[0:5]
write_tb1_time_span = time_span[0:5]

df3 = pd.DataFrame({'热度排名': [i for i in range(1, 6)], '问题ID': question_list[0:5], '热度指数': write_tb1_hot_score,
                    '时间范围': write_tb1_time_span, '地点/人群': write_tb1_loc_people, '问题描述': write_tb1_abb},
                   columns=['热度排名', '问题ID', '热度指数', '时间范围', '地点/人群', '问题描述'])
df3.to_excel(out_path3, index=None)
print('导出文件: ', out_path3)
