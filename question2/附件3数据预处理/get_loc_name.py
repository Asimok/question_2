"""
提取附件2中出现的 X市、X县等信息 生成jieba用户自定义次词典
输入文件：
附件2.xlsx
输出文件：
places.txt
"""

import re

import pandas as pd

path = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/附件2.xlsx'
outpath = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/places.txt'
df = pd.read_excel(path, usecols=[2, 4], names=None)
df_li = df.values.tolist()
# 提取特有地名到用户自建词表
ress = []
pattern = re.compile(r'[A-Z]{1}[0-9]*[\u7701|\u5e02|\u533a|\u53bf|\u4e61|\u6751|\u9547]{1}')
for s_li in df_li:
    res_top = pattern.findall(s_li[0])
    res_con = pattern.findall(s_li[1])
    res_top = res_top + res_con
    ress = ress + res_top
ress = list(set(ress))
print(ress)
with open(outpath, 'w') as f:
    for user_want in ress:
        f.write(user_want)
        f.write(' ')
        f.write('ns')
        f.write('\n')
