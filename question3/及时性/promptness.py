"""
计算留言回复的及时性
输入文件：
附件4_清洗后.xlsx
输出文件：
及时性.xls
"""
import pandas as pd

from question2.附件3数据预处理.date_format import get_date_interval

outpath = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/data/及时性.xls'

data = pd.read_excel('/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/data/附件4_清洗后.xlsx')

message_time = list(data['留言时间'])
reply_time = list(data['答复时间'])

# 答复时间间隔
interval = []
for i in range(len(reply_time)):
    temp_interval = get_date_interval(message_time[i], reply_time[i])
    interval.append(temp_interval)


# 划分标准
def get_evaluate(temp_num):
    if temp_num == 0:
        return 'A+'
    elif temp_num < 4:
        return 'A'
    elif temp_num < 7:
        return 'B'
    elif temp_num < 30:
        return 'C'
    elif temp_num < 360:
        return 'D'
    else:
        return 'E'


evaluate = []
for i in interval:
    temp_evaluate = get_evaluate(i)
    evaluate.append(temp_evaluate)

# 写入数据
write_data = pd.DataFrame({'留言编号': data['留言编号'], '回复间隔': interval, '及时性评价': evaluate, },
                          columns=['留言编号', '回复间隔', '及时性评价'])
write_data.to_excel(outpath, index=None)
print('导出', outpath)
