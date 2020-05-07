"""
对附件3进行数据预处理
预处理内容：
统一时间格式、日期规范化、去除无关符号
输入文件：
附件3.xlsx
输出文件：
附件3_清洗后.xlsx
"""

import pandas as pd

print('开始进行附件3数据预处理')
cols = ['留言编号', '留言用户', '留言主题', '留言时间', '留言详情', '反对数', '点赞数']

path = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/附件3.xlsx'
outpath = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/附件3_清洗后.xlsx'
data = pd.read_excel(path)

user_df_end = pd.DataFrame(columns=cols)
# 统一时间格式
message_time = data['留言时间']
message_time = message_time.apply(lambda x: str(x).strip().replace('-', '/'))
# 日期规范化
for i in range(len(data['留言时间'])):
    if not str(message_time[i]).strip().__contains__(':'):
        message_time[i] = str(message_time[i]).strip() + ' 00:00:00'

data['留言时间'] = message_time
# 去除无关符号
data['留言详情'] = data['留言详情'].apply(
    lambda x: str(x).strip().replace('\r', '').replace('\n', '').replace('\t', '').replace('\u3000', '').replace(
        '\xa0', ''))
data['留言主题'] = data['留言主题'].apply(
    lambda x: str(x).strip().replace('\r', '').replace('\n', '').replace('\t', '').replace('\u3000', '').replace(
        '\xa0', ''))

# 导出数据
data.to_excel(outpath, columns=cols)
print('导出数据: ', outpath)
print('附件3数据预处理完成')
