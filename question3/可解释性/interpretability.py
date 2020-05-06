# 计算留言回复的完整性

import pandas as pd
from textrank4zh import TextRank4Sentence

from question3.可解释性.sentence_similarity import tf_similarity

outpath = '../data/附件4_留言主题句+答复主题句+可解释性.xlsx'
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
        # print(abstract)
    return abb


reply_abb = get_abstract(reply)
message_abb = get_abstract(message)
data['答复意见_主题句'] = reply_abb
data['留言详情_主题句'] = message_abb
similarity = []
for i in range(len(reply_abb)):
    temp_similarity = tf_similarity(message_abb[i], reply_abb[i])
    similarity.append(temp_similarity)

data['可解释性'] = similarity
data.to_excel(outpath)
print('导出', outpath)
