"""
根据用户ID分类留言
对同一用户30天内，相似度高于0.75的留言去重
保证聚类结果的准确性
输入文件：
附件3_清洗后.xlsx
输出文件：
去除30天内同一用户相似度0.75+的留言.xls
"""

import pandas as pd

from question2.附件3数据预处理.date_format import get_date_interval
from question2.附件3数据预处理.sentence_similarity import tf_similarity

print('执行  path_data_cleansing.py')
cols = ['留言编号', '留言用户', '留言主题', '留言时间', '留言详情', '反对数', '点赞数']

path = ' /home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/附件3_清洗后.xlsx'
outpath = ' /home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/去除30天内同一用户相似度0.75+的留言.xls'
data = pd.read_excel(path)

user_df_end = pd.DataFrame(columns=cols)


# 去重复
def remove_user_themes(temp_list_fun, interval_day, similarity):
    global user_df_end
    del_theme = []  # 记录待删除留言
    # data2 = user_list[47].reset_index()
    data2 = temp_list_fun.reset_index()
    theme_len = len(data2['留言主题'])
    temp_data = data2['留言主题']
    for i in range(theme_len):
        d1 = data2['留言时间'][i]
        for j in range(i + 1, theme_len):
            temp_similarity = tf_similarity(temp_data[i], temp_data[j])
            if temp_similarity > similarity:
                # 保留日期近的 30天内不可重复留言
                print(temp_data[i], temp_data[j], temp_similarity)
                d2 = data2['留言时间'][j]
                temp_days = get_date_interval(d1, d2)
                if temp_days >= 0 & temp_days <= interval_day:
                    del_theme.append(i)
                elif temp_days >= -interval_day & temp_days < 0:
                    del_theme.append(j)
    del_theme = list(set(del_theme))
    for i in del_theme:
        data2.drop(labels=i, inplace=True)
    data2.reset_index(inplace=True)
    data2.drop(labels=['level_0', 'index'], inplace=True, axis=1)
    user_df_end = pd.concat([user_df_end, data2], axis=0)


user = data['留言用户']
alluser = list(user)
gp = data.groupby(user)
user_dict = {}
for temp_user in alluser:
    df = gp.get_group(temp_user)
    user_dict[temp_user] = df
user_list = []
for value in user_dict.values():
    user_list.append(value)

for temp_list in user_list:
    if len(temp_list) > 1:
        # print('筛选')
        remove_user_themes(temp_list, 30, 0.75)
    else:
        # user_list_end.append(temp_list)
        user_df_end = pd.concat([user_df_end, temp_list], axis=0)

user_df_end.to_excel(outpath, index=None)
print('导出数据: ', outpath)
print('执行  path_data_cleansing.py 完成')
