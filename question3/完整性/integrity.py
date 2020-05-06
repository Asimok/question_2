# 计算留言回复的完整性

import re
from textrank4zh import TextRank4Sentence, TextRank4Keyword

import pandas as pd

data = pd.read_excel('../data/附件4.xlsx')
reply = data['答复意见']
message = data['留言详情']


# 查找统计中括号字符
def get_ans_str(string):
    p1 = re.compile(r'[《](.*?)[》]', re.S)  # 最小匹配
    temp_ans_list = []
    temp_ans_str = ''
    for i in re.findall(p1, string):
        temp_ans_list.append('《' + str(i) + '》')
        temp_ans_str += '《' + str(i) + '》'
    return temp_ans_str, temp_ans_list


contain_law = []
for i in reply:
    ans_str, ans_list = get_ans_str(i)
    contain_law.append(ans_str)
data['法律法规'] = contain_law


# 提取 留言详情 答复意见 主题句
def get_abstract(temp_data):
    abb = []
    for abb_str in temp_data:
        sentence = TextRank4Sentence()
        sentence.analyze(text=abb_str, lower=True)
        abstract = '\n'.join([item.sentence for item in sentence.get_key_sentences(num=1)])
        abb.append(abstract)
        print(abstract)
    return abb


data['答复意见_主题句'] = get_abstract(reply)
data['留言详情_主题句'] = get_abstract(message)
data.to_excel('../data/附件4_法律法规+主题.xlsx')
