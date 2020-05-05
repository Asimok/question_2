from __future__ import print_function, unicode_literals
import json
import requests


NER_URL = 'http://api.bosonnlp.com/ner/analysis'


s = ['对于该小孩是不是郑尚金的孩子，目前已做亲子鉴定，结果还没出来，'
     '纪检部门仍在调查之中。成都商报记者 姚永忠']
data = json.dumps(s)
headers = {
    'X-Token': 'YOUR_API_TOKEN',
    'Content-Type': 'application/json'
}
resp = requests.post(NER_URL, headers=headers, data=data.encode('utf-8'))


for item in resp.json():
    for entity in item['entity']:
        print(''.join(item['word'][entity[0]:entity[1]]), entity[2])