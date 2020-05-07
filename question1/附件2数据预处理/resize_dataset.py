# 分割  训练集 验证集 测试集
import pandas as pd

print('分割  训练集 验证集 测试集')
classification = ['城乡建设', '环境保护', '交通运输', '教育文体', '劳动和社会保障', '商贸旅游', '卫生计生']
data = pd.read_excel('/home/asimov/PycharmProjects/wisdom_gov_affairs/question1/data/附件2_清洗后.xlsx')
classification_num = list(data['一级标签'].value_counts())
test = []
y_test = []
train = []
y_train = []
dev = []
y_dev = []


def get_temp_val(data_train, data_test, data_dev):
    for index in data_train['留言详情']:
        train.append(str(index).strip())
    for index in data_train['一级标签']:
        y_train.append(classification.index(index))
    for index in data_test['留言详情']:
        test.append(
            str(index).strip())
    for index in data_test['一级标签']:
        y_test.append(classification.index(index))

    for index in data_dev['留言详情']:
        dev.append(
            str(index).strip())
    for index in data_dev['一级标签']:
        y_dev.append(classification.index(index))


# 训练集 验证集 测试集 0.15 0
# 比例 6:2:2
for i in range(len(classification)):
    get_temp_data = data.loc[data['一级标签'] == classification[i]]
    temp_data = get_temp_data.sample(frac=0.4)
    temp_train = get_temp_data.drop(temp_data.index)
    temp_test = temp_data.sample(frac=0.5)
    temp_dev = temp_data.drop(temp_test.index)
    get_temp_val(temp_train, temp_test, temp_dev)

# 打乱顺序
end_data_train = pd.DataFrame({'data': train, 'label': y_train})
end_data_train = end_data_train.sample(frac=1).reset_index(drop=True)
train_end = end_data_train['data']
y_train_end = end_data_train['label']

end_data_test = pd.DataFrame({'data': test, 'label': y_test})
end_data_test = end_data_test.sample(frac=1).reset_index(drop=True)
test_end = end_data_test['data']
y_test_end = end_data_test['label']

end_data_dev = pd.DataFrame({'data': dev, 'label': y_dev})
end_data_dev = end_data_dev.sample(frac=1).reset_index(drop=True)
dev_end = end_data_dev['data']
y_dev_end = end_data_dev['label']

path = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question1/data/'

name = "detail"
with open(path + 'train_' + name + '.txt', 'w') as f:
    for i in range(len(y_train_end)):
        f.write(str(train_end[i]))
        f.write('\t')
        f.write(str(y_train_end[i]))
        f.write('\n')
with open(path + 'test_' + name + '.txt', 'w') as f:
    for i in range(len(y_test_end)):
        f.write(str(test_end[i]))
        f.write('\t')
        f.write(str(y_test_end[i]))
        f.write('\n')
with open(path + 'dev_' + name + '.txt', 'w') as f:
    for i in range(len(y_dev_end)):
        f.write(str(dev_end[i]))
        f.write('\t')
        f.write(str(y_dev_end[i]))
        f.write('\n')

lens = []

for i in range(data['留言详情'].__len__()):
    lens.append(len(data['留言详情'][i]))
shapes = pd.DataFrame(lens).describe()
print('完成分割  训练集 验证集 测试集')
