# 根据用户ID分类留言
import pandas as pd

cols = ['留言编号', '留言用户', '留言主题', '留言时间', '留言详情', '反对数', '点赞数']

path = '../data/附件3.xlsx'
outpath = '../data/附件3_清洗后.xlsx'
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
