# 计算留言回复的完整性

import pandas as pd
from textrank4zh import TextRank4Sentence

data = pd.read_excel('../data/附件4_清洗后.xlsx')
reply = data['答复意见']
message = data['留言详情']


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
data.to_excel('../data/附件4_留言主题句+答复主题句.xlsx')
