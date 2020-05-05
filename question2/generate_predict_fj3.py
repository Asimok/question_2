import pandas as pd

data = pd.read_excel('/home/asimov/PycharmProjects/wisdom_gov_affairs/question2/data/附件3.xlsx', sheet_name='Sheet1')

predict_data = []

for index in data['留言详情']:
    predict_data.append(
        str(index).strip().replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '').replace('\u3000',
                                                                                                          '').replace(
            '*',
            '').replace(
            '\xa0', ''))

path = '/home/asimov/PycharmProjects/Chinese-Text-Classification-Pytorch/THUCNews/data/'
# path='/home/asimov/PycharmProjects/wisdom_gov_affairs/C_data/processed/'
name = "data"
with open(path + 'predict_' + name + '.txt', 'w') as f:
    for i in range(len(predict_data)):
        f.write(str(predict_data[i]))
        f.write('\t')
        f.write('0')
        f.write('\n')

