import jieba.analyse
import pandas as pd
import numpy as np
import jieba.analyse
import jieba.posseg as psg
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import DBSCAN

from question2.数据清洗.date_format import get_date_interval
path = '/home/asimov/PycharmProjects/question_2/question2/数据清洗/示例数据_去除30天内同一用户相似度0.75+的留言.xls'
# path='/home/asimov/PycharmProjects/question_2/question2/数据清洗/去除30天内同一用户相似度0.75+的留言.xls'
pos_com = pd.read_excel(path)
all_data = pd.read_excel(path)
predict_data = []

for index in pos_com['留言主题']:
    predict_data.append(
        str(index).strip().replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '').replace('\u3000',
                                                                                                          '').replace(
            '*',
            '').replace(
            '\xa0', ''))
"""
l:习用语 nr:人名 nz:其他专名 ns:地名
"""
jieba.load_userdict('../data/new_places.txt')
jieba.load_userdict('../data/changsha_ns.txt')

data_cut = pd.Series(predict_data).apply(lambda x: jieba.lcut(x))
# 去除停用词 csv 默认 ,作为分隔符 用sep取一个数据里不存在的字符作为分隔符保障顺利读取
stop_words = pd.read_csv('../data/stopword.txt', sep='hhhh', encoding='GB18030', engine='python')
# pd转列表拼接  iloc[:,0] 取第0列
stop_words = list(stop_words.iloc[:, 0]) + [' ', '...', '', '  ', '→', '-', '：', ' ●', '\t', '\n', '！', '？']
data_after_stop = data_cut.apply(lambda x: [i.strip() for i in x if i not in stop_words])

word2flagdict = {}
PEOPLE_AND_LOC = []
for temp_theme in predict_data:
    data_cut = psg.cut(temp_theme)
    data_after_stop = []
    for i in data_cut:
        if i not in stop_words:
            if i != "":
                data_after_stop.append(i.word)
                word2flagdict[i.word] = i.flag
    keywords = " ".join(data_after_stop)
    PEOPLE_AND_LOC.append(keywords)
# all_data['主题分词'] = PEOPLE_AND_LOC
# all_data.to_excel('/home/asimov/PycharmProjects/question_2/question2/聚类分析/附件3_labels.xlsx', index=None)

# 自己造一个{“词语”:“词性”}的字典，方便后续使用词性
# word2flagdict = {wordtocixing[i]:cixingofword[i] for i in range(len(wordtocixing))}
# 短文本特征提取
vectorizer = CountVectorizer()
transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
# 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
tfidf = transformer.fit_transform(vectorizer.fit_transform(PEOPLE_AND_LOC))
# 获取词袋模型中的所有词语
word = vectorizer.get_feature_names()
# 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
weight = tfidf.toarray()

# 我们将word中每个词语的词性，通过自定义的方式赋给它们不同的权重，并乘到weight上的每一行样本中，
# 进而改变它们的特征矩阵。这样做的目的其实是想让特征矩阵的区分能力增强一点，代码如下所示：
wordflagweight = [1 for i in range(len(word))]  # 这个是词性系数，需要调整系数来看效果
for i in range(len(word)):
    if word2flagdict.get(word[i]) == "n":  # 这里只是举个例子，名词重要一点，我们就给它1.1
        wordflagweight[i] = 1.0
    # elif word2flagdict.get(word[i]) == "ns":
    #     wordflagweight[i] = 1.1
    else:  # 权重数值还要根据实际情况确定，更多类型还请自己添加
        continue

wordflagweight = np.array(wordflagweight)
newweight = weight.copy()
for i in range(len(weight)):
    for j in range(len(word)):
        newweight[i][j] = weight[i][j] * wordflagweight[j]

hot_score = []  # 热度指数
write_cluster_detail = []
write_cluster_theme = []
write_cluster_id = []
write_cluster_user = []
write_cluster_detail_id = []
write_cluster_time = []
temp_detail = list(pos_com['留言详情'])
temp_theme = list(pos_com['留言主题'])
temp_user = list(pos_com['留言用户'])
temp_id = list(pos_com['留言编号'])
temp_time = list(pos_com['留言时间'])
# DBSCAN聚类分析

DBS_clf = DBSCAN(eps=1.3, min_samples=4)
DBS_clf.fit(newweight)
labels_ = DBS_clf.labels_


# === Define the function of classify the original corpus according to the labels === #
def labels_to_original(labels, original_corpus):
    assert len(labels) == len(original_corpus)
    max_label = max(labels)
    number_label = [i for i in range(0, max_label + 1, 1)]
    number_label.append(-1)
    result = [[] for i in range(len(number_label))]
    result_loc = [[] for i in range(len(number_label))]
    for labels_loc in range(len(labels)):
        res_index = number_label.index(labels[labels_loc])
        result[res_index].append(original_corpus[labels_loc])
        result_loc[res_index].append(labels_loc)
    return result, result_loc


def get_interval(temp_loc_list):
    # 去除1年之外的数据
    # min_date = '2099/12/31 00:00:00'
    # max_date = '2000/12/01 00:00:00'
    min_date = temp_time[0]
    max_date = temp_time[0]
    # 找到最大日期
    for loc in temp_loc_list:
        temp_max = get_date_interval(max_date, temp_time[loc])

        if temp_max > 0 & temp_max < 360:
            max_date = temp_time[loc]
    for loc in temp_loc_list:
        temp_min = get_date_interval(temp_time[loc], min_date)
        if temp_min > 0 and (get_date_interval(temp_time[loc],max_date) < 360):
            print(temp_min,get_date_interval(temp_time[loc],max_date))
            min_date = temp_time[loc]
    print('最小日期   ', min_date)
    print('最大日期   ',max_date)
    return get_date_interval(min_date, max_date)


labels_original, labels_loc = labels_to_original(labels_, PEOPLE_AND_LOC)
# for i in range(5):
#     print(labels_original[i])
# get_interval(labels_loc[13])

for i in range(len(labels_loc) - 1):
    # 时间跨度
    temp_interval = get_interval(labels_loc[i])
    # 留言数量
    message_num = len(labels_loc[i])
    # 单位热度
    temp_hot = message_num / temp_interval
    hot_score.append(temp_hot)
    for j in labels_loc[i]:
        write_cluster_detail.append(temp_detail[j])
        write_cluster_theme.append(temp_theme[j])
        write_cluster_detail_id.append(i)
        write_cluster_id.append(temp_id[j])
        write_cluster_user.append(temp_user[j])
        write_cluster_time.append(temp_time[j])
        hot_score.append("  ")
    write_cluster_detail.append("   ")
    write_cluster_theme.append("   ")
    write_cluster_detail_id.append("   ")
    write_cluster_id.append("   ")
    write_cluster_user.append("   ")
    write_cluster_time.append("   ")
write_cluster_detail_xls = pd.DataFrame(
    {"热度指数": hot_score, "聚类ID": write_cluster_detail_id, '留言主题': write_cluster_theme, '留言详情': write_cluster_detail,
     '留言编号': write_cluster_id, '留言用户': write_cluster_user, '留言时间': write_cluster_time},
    columns=["热度指数", '聚类ID', '留言编号', '留言用户', '留言时间', '留言主题', '留言详情'])
outpath = './示例数据_聚类_主题_去重_热度_0.9_4.xls'
write_cluster_detail_xls.to_excel(outpath, index=None)
print(outpath, '导出成功!!!')
