import jieba.analyse
import jieba.posseg as psg
jieba.load_userdict('../data/new_places.txt')
jieba.load_userdict('../data/new_places_country.txt')
jieba.load_userdict('../data/weibo_jieba.txt')
str = '反映M9县春华镇金鼎村水泥路、自来水到户的问题'
print(str)
keywords = " ".join(
    jieba.analyse.extract_tags(sentence=str, topK=10, withWeight=False, allowPOS=(['n', 'ns', 'l', 'nr', 'nz'])))
print(keywords)
keywords = jieba.analyse.extract_tags(sentence=str, topK=5, withWeight=True, allowPOS=(['n', 'v']))
print(keywords)

print('分词及词性：')
result = psg.cut(str)
print([(x.word, x.flag) for x in result])
