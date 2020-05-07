"""
根据评价机制生成留言答复评价指标
输入文件：
及时性.xls、可解释性.xls、完整性.xls、相关性.xls
输出文件：
评价方案.xls
"""
import math

import pandas as pd

outpath = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/answer3/评价方案.xls'
data_promptness = pd.read_excel('/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/data/及时性.xls')
data_interpretability = pd.read_excel('/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/data/可解释性.xls')
data_integrity = pd.read_excel('/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/data/完整性.xls')
data_correlation = pd.read_excel('/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/data/相关性.xls')

proj_sol = data_interpretability['可解释性评价'].tolist()
proj_rel = data_correlation['相关性评价'].tolist()
proj_tim = data_promptness['及时性评价'].tolist()
proj_ful = data_integrity['完整性评价'].tolist()
level_num = []
level_word = []


def change_value(proj):
    if proj == "A+":
        proj = 1.0
    elif proj == "A":
        proj = 0.8
    elif proj == 'B':
        proj = 0.6
    elif proj == 'C':
        proj = 0.4
    elif proj == 'D':
        proj = 0.2
    elif proj == 'E':
        proj = 0.0
    return proj


def check_level(proj_A, proj_B, proj_C, proj_D):
    for i in range(len(proj_A)):
        flag_EA = 0  # 判断E在不在
        flag_EB = 0
        flag_EC = 0
        flag_ED = 0
        flag_A = 0  # 判断A+是否存在
        if proj_A[i] == "A+":
            flag_A = 1
        elif proj_A[i] == "E":
            flag_EA = 1
        elif proj_B[i] == "A+":
            flag_A = 1
        elif proj_B[i] == "E":
            flag_EB = 1
        elif proj_C[i] == "A+":
            flag_A = 1
        elif proj_C[i] == "E":
            flag_EC = 1
        elif proj_D[i] == "A+":
            flag_A = 1
        elif proj_D[i] == "A+":
            flag_ED = 1
        # 单词转数字
        A = change_value(proj_A[i])
        B = change_value(proj_B[i])
        C = change_value(proj_C[i])
        D = change_value(proj_D[i])
        num = 0.3 * (A + B) + 0.2 * (C + D)  # 基础权重
        print(i, '基础权重', num)
        num = num - 0.3 * (flag_EA * 0.1 + flag_EB * 0.1) - 0.2 * (flag_EC * 0.1 + flag_ED * 0.1)  # 含E权重
        print(i, 'E权重', num)
        num = int(num * 100) / 100
        print(i, "整型", num)
        # version
        if flag_A == 1:
            num = (math.ceil(num * 10)) / 10
            print(i, 'A权重', num)  #
        else:
            num = round(num * 10) / 10
            print(i, '四舍五入权重', num)
        num = num * 10
        if num % 2 != 0:
            print("#", num)
            num = (num - 1) / 10
        else:
            num = num / 10
        print("输出", num)
        level_num.append(num)
        if num == 0:
            level_word.append('E')
        elif num == 0.2:
            level_word.append('D')
        elif num == 0.4:
            level_word.append('C')
        elif num == 0.6:
            level_word.append('B')
        elif num == 0.8:
            level_word.append('A')
        elif num == 1:
            level_word.append('A+')


check_level(proj_sol, proj_rel, proj_tim, proj_ful)
cols = ['留言编号', '相关性', '完整性', '可解释性', '及时性', '权值', '评级']
data = pd.DataFrame({'留言编号': data_promptness['留言编号'], '相关性': data_correlation['相关性评价'],
                     '完整性': data_integrity['完整性评价'],
                     '可解释性': data_interpretability['可解释性评价'], '及时性': data_promptness['及时性评价'], '权值': level_num,
                     '评级': level_word}, columns=cols)
data.to_excel(outpath, index=None)
print('导出文件', outpath)
