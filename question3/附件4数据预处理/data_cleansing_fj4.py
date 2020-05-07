# 根据用户ID分类留言
import pandas as pd

cols = ['留言编号', '留言用户', '留言主题', '留言时间', '留言详情', '答复意见', '答复时间']

path = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/data/附件4.xlsx'
outpath = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/data/附件4_清洗后.xlsx'
data = pd.read_excel(path)

user_df_end = pd.DataFrame(columns=cols)
# 统一时间格式
message_time = data['留言时间']
reply_time = data['答复时间']
message_time = message_time.apply(lambda x: str(x).strip().replace('-', '/'))
reply_time = reply_time.apply(lambda x: str(x).strip().replace('-', '/'))
# 日期规范化
for i in range(len(data['留言时间'])):
    if not str(message_time[i]).strip().__contains__(':'):
        message_time[i] = str(message_time[i]).strip() + ' 00:00:00'
    if not str(reply_time[i]).strip().__contains__(':'):
        reply_time[i] = str(reply_time[i]).strip() + ' 00:00:00'
data['留言时间'] = message_time
data['答复时间'] = reply_time
# 去除无关符号
data['留言详情'] = data['留言详情'].apply(
    lambda x: str(x).strip().replace('\r', '').replace('\n', '').replace('\t', '').replace('\u3000', '').replace(
        '\xa0', ''))
data['答复意见'] = data['答复意见'].apply(
    lambda x: str(x).strip().replace('\r', '').replace('\n', '').replace('\t', '').replace('\u3000', '').replace(
        '\xa0', ''))
data['留言主题'] = data['留言主题'].apply(
    lambda x: str(x).strip().replace('\r', '').replace('\n', '').replace('\t', '').replace('\u3000', '').replace(
        '\xa0', ''))

# 导出数据
data.to_excel(outpath, columns=cols)
