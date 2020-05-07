"""
提取文件的标准开头结尾
输入参数：
句子temp_str
返回参数：
句子标准开头结尾 temp_header, temp_tail
"""


def find_last(string, temp_str):
    last_position = -1
    while True:
        position = string.find(temp_str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position


def get_head_tail(temp_str):
    temp_header = ''
    temp_tail = ''
    if str(temp_str).__contains__('如下：'):
        temp = temp_str[0:str(temp_str).index('如下：') + 3]
        temp_str = str(temp_str).replace(temp, '')
        if len(temp) < 80:
            temp_header += temp
    if str(temp_str).__contains__('回复：'):
        temp = temp_str[0:str(temp_str).index('回复：') + 3]
        temp_str = str(temp_str).replace(temp, '')
        if len(temp) < 80:
            temp_header += temp
    if str(temp_str).__contains__('感谢您对'):
        temp = temp_str[find_last(temp_str, '感谢您对'):]
        if len(temp) < 80:
            temp_tail += temp
    return temp_header, temp_tail
