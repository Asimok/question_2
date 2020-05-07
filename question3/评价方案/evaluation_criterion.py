# 评价标准
from itertools import combinations_with_replacement

import pandas as pd

com = list(combinations_with_replacement(['A+', 'A', 'B', 'C', 'D', 'E'], 4))  # 列举组合结果
com_list = []
for i in com:
    com_list.append(list(i))
data = pd.DataFrame({'组合': com_list})
data.to_excel('/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/data/评价组合.xls', index=None)
