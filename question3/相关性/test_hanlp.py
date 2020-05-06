import hanlp
import jieba.analyse
import jieba.posseg as psg

tokenizer = hanlp.load('PKU_NAME_MERGED_SIX_MONTHS_CONVSEG')

recognizer = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)

A = recognizer.predict([list('关于A市地铁7号线的相关建议')])
print(A)

jieba.load_userdict('../data/places.txt')
jieba.load_userdict('../data/changsha_transportation_ns.txt')
jieba.load_userdict('../data/changsha_houses_ns.txt')
jieba.load_userdict('../data/changsha_area_ns.txt')

"""
l:习用语 nr:人名 nz:其他专名 ns:地名
"""
a = jieba.analyse.extract_tags(sentence='咨询A市人才购房补贴通知问题', topK=4, withWeight=False,
                               allowPOS=(['ns', 'nz', 'nr']))
print(a)

print('分词及词性：')
result = psg.lcut('咨询A市人才购房补贴通知问题')
print([(x.word, x.flag) for x in result])
