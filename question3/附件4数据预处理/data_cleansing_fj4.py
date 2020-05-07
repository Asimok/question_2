"""
对附件2进行数据预处理
预处理内容：
统一时间格式、日期规范化、去除无关符号、 去除标准开头结尾、判断是否包含机构
输入文件：
附件4.xlsx
输出文件：
附件4_清洗后.xlsx
"""
import hanlp
import pandas as pd

from question3.相关性.get_head_tail import get_head_tail

cols = ['留言编号', '留言用户', '留言主题', '留言时间', '留言详情', '答复意见', '答复时间', '是否包含机构']

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

read_reply = data['答复意见']
reply = []
# 去除标准开头结尾
for i in read_reply:
    head, tail = get_head_tail(i)
    temp_str = str(i).replace(head, '')
    temp_str = temp_str.replace(tail, '')
    reply.append(temp_str)

# 是否包含机构
contain_nt_list = []
recognizer = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)
for i in range(len(reply)):
    print(i)
    contain_nt = False
    for simple_str in str(reply[i]).split('，'):
        recognizer_nt = recognizer.predict([list(simple_str)])
        for nt_id in recognizer_nt:
            for j in nt_id:
                if j[1] == 'NT':
                    contain_nt = True
                    contain_nt_list.append(contain_nt)
                    break
            if contain_nt:
                break
        if contain_nt:
            break
    if not contain_nt:
        contain_nt_list.append(contain_nt)
data['是否包含机构'] = contain_nt_list
# 导出数据
data.to_excel(outpath, columns=cols)
