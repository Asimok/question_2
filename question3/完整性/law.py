# 计算留言回复的完整性

import re

import pandas as pd

data = pd.read_excel('../data/附件4.xlsx')
reply = data['答复意见']
message = data['留言详情']


# 查找统计中括号字符
def get_ans_str(string):
    p1 = re.compile(r'[《](.*?)[》]', re.S)  # 最小匹配
    temp_ans_list = []
    temp_ans_str = ''
    for i in re.findall(p1, string):
        temp_ans_list.append('《' + str(i) + '》')
        temp_ans_str += '《' + str(i) + '》'
    return temp_ans_str, temp_ans_list


contain_law = []
for i in reply:
    ans_str, ans_list = get_ans_str(i)
    contain_law.append(ans_str)
data['法律法规'] = contain_law

data.to_excel('../data/法律法规.xlsx')
