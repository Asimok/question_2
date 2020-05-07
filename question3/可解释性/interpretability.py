# 计算留言回复的完整性
import re

import pandas as pd

from question3.相关性.get_head_tail import get_head_tail

outpath = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/data/可解释性.xls'
data = pd.read_excel('/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/data/附件4_清洗后.xlsx')
read_reply = data['答复意见']
fact = pd.read_csv('/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/data/事实依据词表.txt',
                   sep='hhhh', engine='python')
fact = list(fact.iloc[:, 0])
data_contain_nt = data['是否包含机构']
reply = []
# 去除标准开头结尾
for i in read_reply:
    head, tail = get_head_tail(i)
    temp_str = str(i).replace(head, '')
    temp_str = temp_str.replace(tail, '')
    reply.append(temp_str)


def contain_law_fun(string):
    p1 = re.compile(r'[《](.*?)[》]', re.S)  # 最小匹配
    temp_ans_list = []
    for temp_law_id in re.findall(p1, string):
        temp_ans_list.append(str(temp_law_id))
    if len(temp_ans_list) > 0:
        return True
    else:
        return False


def contain_fact_fun(string):
    for fact_id in fact:
        if str(string).__contains__(fact_id):
            return True
    return False


def generate_score(temp_nt, temp_law, temp_fact):
    if temp_fact and temp_law and temp_nt:
        return 'A+'
    elif temp_fact and temp_law:
        return 'A'
    elif temp_law:
        return 'B'
    elif temp_fact:
        return 'C'
    elif temp_nt:
        return 'D'
    else:
        return 'E'


# 机构 事实依据 法律法规
score = []

for i in range(len(reply)):
    contain_law = contain_law_fun(reply[i])
    contain_fact = contain_fact_fun(reply[i])
    score.append(generate_score(bool(data_contain_nt[i]), contain_law, contain_fact))

write_data = pd.DataFrame({'可解释性评价': score, '留言编号': data['留言编号']}, columns=['留言编号', '可解释性评价'])
write_data.to_excel(outpath, index=None)
print('导出', outpath)
