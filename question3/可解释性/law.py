"""
提取附件4 答复意见 中的法律法规、政策文件等
输入文件：
附件4_清洗后.xlsx
输出文件：
法律法规.xls
"""
import re

import pandas as pd

data = pd.read_excel('/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/data/附件4_清洗后.xlsx')
reply = data['答复意见']


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

data.to_excel(outpath, index=None)
