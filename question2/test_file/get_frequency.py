"""
获得留言主题的词频
"""

import matplotlib.pyplot  as plt
import pandas as pd
from wordcloud import WordCloud

data = pd.read_excel('./classifications_seven_PEOPLE_AND_LOC/教育文体——地点_人群_主题.xls')
data_after = []
for temp_theme in data['地点/人群']:
    for i in str(temp_theme).split(' '):
        if i != ' ':
            data_after.append(i)  # 去除空格

frequency = pd.Series(data_after).value_counts()  # 转为序列 统计
word_sum = frequency.sum()
frequency_dict = dict(frequency)
for key, value in frequency_dict.items():
    frequency_dict[key] = (frequency_dict[key] / word_sum) * 1000

"""
句子得分
"""
data_score = []
for temp_theme in data['地点/人群']:
    temp_score = 0
    for i in str(temp_theme).split(' '):
        if i != ' ':
            temp_score = temp_score + frequency_dict[i]
    data_score.append(round(temp_score, 4))
# data_score=pd.DataFrame({'热度指数':data_score})
data['热度指数'] = data_score
data = data.sort_values("热度指数", inplace=False, ascending=False)
data.to_excel('./classifications_seven_PEOPLE_AND_LOC/教育文体——地点_人群_主题.xls', index=None)

# ----------------------------------词云-------------------------------------
mask = plt.imread('./data/duihuakuan.jpg')
wc = WordCloud(font_path='/usr/share/fonts/opentype/noto/NotoSerifCJK-Medium.ttc', mask=mask, background_color='white')
wc.fit_words(frequency_dict)
plt.imshow(wc)
# plt.imsave('word.png', wc)
plt.axis('off')
plt.show()
