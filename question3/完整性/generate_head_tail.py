# 提取文件的标准开头结尾

import pandas as pd

data = pd.read_excel('../data/附件4_清洗后.xlsx')
reply = data['答复意见']


def find_last(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position


header = []
tail = []
for i in reply:
    temp_header = ''
    temp_tail = ''
    if str(i).__contains__('如下：'):
        temp = i[0:str(i).index('如下：') + 3]
        i = str(i).replace(temp, '')
        if len(temp) < 80:
            temp_header += temp
    if str(i).__contains__('回复：'):
        temp = i[0:str(i).index('回复：') + 3]
        i = str(i).replace(temp, '')
        if len(temp) < 80:
            temp_header += temp
    if str(i).__contains__('感谢您对'):
        temp = i[find_last(i, '感谢您对'):]
        if len(temp) < 80:
            temp_tail += temp
    header.append(temp_header)
    tail.append(temp_tail)
write_data = pd.DataFrame({'开头': header, '结尾': tail})

write_data.to_excel('../data/开头结尾.xls', index=None)
