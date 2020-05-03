import re

import jieba.analyse
import pandas as pd

classification = ['城乡建设', '环境保护', '交通运输', '教育文体', '劳动和社会保障', '商贸旅游', '卫生计生']
data = pd.read_excel('/home/asimov/PycharmProjects/question_2/question2/data/附件3.xlsx', sheet_name='Sheet1')

theme_data = data['留言主题']
detail_data = data['留言详情']

# 合并留言主题 和留言详情
data['留言合并'] = theme_data + detail_data
# 去除 \t \n
data_all = data['留言合并'].apply(lambda x: re.sub('\n', '', re.sub('\t', '', x)))
# jieba 分词
jieba.load_userdict('./data/new_places.txt')
jieba.load_userdict('./data/changsha_ns.txt')
data_cut = data_all.apply(lambda x: jieba.lcut(x))
# 去除停用词 csv 默认 ,作为分隔符 用sep取一个数据里不存在的字符作为分隔符保障顺利读取
stop_words = pd.read_csv('./data/stopword.txt', sep='hhhh', encoding='GB18030', engine='python')
# pd转列表拼接  iloc[:,0] 取第0列
stop_words = list(stop_words.iloc[:, 0]) + [' ', '...', '', '  ', '→', '-', '：', ' ●', '\t', '\n']
data_after_stop = data_cut.apply(lambda x: [i.strip() for i in x if i not in stop_words])
# data_after_stop = data_after_stop.apply(lambda x: [i.strip() for i in x if i not in list(stop_words2.iloc[:, 0])])
# 去除空格
data_after_stop = data_after_stop.apply(lambda x: [i for i in x if i != ''])

places_cz = []  # 村镇
future_list = ['城', '村', '镇']
for temp_data in data_after_stop:
    for j in temp_data:
        # if str(j) == '城':
        #     temp_place = temp_data[temp_data.index('城') - 1] + temp_data[temp_data.index('城')]
        #     places_cz.append(temp_place)
        # elif str(j) == '村':
        #     temp_place = temp_data[temp_data.index('村') - 1] + temp_data[temp_data.index('村')]
        #     places_cz.append(temp_place)
        # elif str(j) == '镇':
        #     temp_place = temp_data[temp_data.index('镇') - 1] + temp_data[temp_data.index('镇')]
        #     places_cz.append(temp_place)
        if str(j) == '街道':
            temp_place = temp_data[temp_data.index('街道') - 1] + temp_data[temp_data.index('街道')]
            places_cz.append(temp_place)
        elif str(j) == '社区':
            temp_place = temp_data[temp_data.index('社区') - 1] + temp_data[temp_data.index('社区')]
            places_cz.append(temp_place)
        # elif str(j) == '铺':
        #     temp_place = temp_data[temp_data.index('铺') - 1] + temp_data[temp_data.index('铺')]
        #     places_cz.append(temp_place)

places_cz_set = set(places_cz)
with open('./data/add_places_shequ_jiedao.txt','w') as f:
    for i in places_cz_set:
        f.write(i)
        f.write(' ')
        f.write('ns')
        f.write('\n')