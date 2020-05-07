import pandas as pd

from question2.附件3数据预处理.sentence_similarity import tf_similarity
from question3.相关性.get_head_tail import get_head_tail

outpath = '../data/相关性.xls'

data = pd.read_excel('/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/data/附件4_清洗后.xlsx')
message_detail = data['留言详情']
read_reply = data['答复意见']
# reply.apply(lambda x: str(x).replace(head, ''))


reply = []
# 去除标准开头结尾
for i in read_reply:
    head, tail = get_head_tail(i)
    temp_str = str(i).replace(head, '')
    temp_str = temp_str.replace(tail, '')
    reply.append(temp_str)
# 相关性
similarity = []
for i in range(len(reply)):
    temp_similarity = tf_similarity(message_detail[i], reply[i])
    similarity.append(temp_similarity)


# similarity.index(0)
# pd.Series(similarity).min()

# 划分标准
def get_evaluate(temp_num):
    if temp_num < 0.1:
        return 'E'
    elif temp_num < 0.2:
        return 'D'
    elif temp_num < 0.55:
        return 'C'
    elif temp_num < 0.8:
        return 'B'
    elif temp_num < 0.9:
        return 'A'
    else:
        return 'A+'


evaluate = []
for i in similarity:
    evaluate.append(get_evaluate(i))

# 写入数据
data['相关性'] = similarity
# data['分词后相关性'] = similarity_jieba
data['相关性评价'] = evaluate
data.to_excel(outpath, index=None)
print('导出', outpath)
