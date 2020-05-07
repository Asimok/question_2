# 提取文件的标准开头结尾


def find_last(string, temp_str):
    last_position = -1
    while True:
        position = string.find(temp_str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position


def get_head_tail(i):
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
    return temp_header, temp_tail
