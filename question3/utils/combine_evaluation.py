import pandas as pd

outpath = '/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/answer3/评价方案.xls'
data_promptness = pd.read_excel('/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/data/及时性.xls')
data_interpretability = pd.read_excel('/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/data/可解释性.xls')
data_integrity = pd.read_excel('/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/data/完整性.xls')
data_correlation = pd.read_excel('/home/asimov/PycharmProjects/wisdom_gov_affairs/question3/data/相关性.xls')
cols = ['留言编号', '相关性', '完整性', '可解释性', '及时性']
data = pd.DataFrame({'留言编号': data_promptness['留言编号'], '相关性': data_correlation['相关性评价'],
                     '完整性': data_integrity['完整性评价'],
                     '可解释性': data_interpretability['可解释性评价'], '及时性': data_promptness['及时性评价']}, columns=cols)
data.to_excel(outpath, index=None)
print('导出文件', outpath)
