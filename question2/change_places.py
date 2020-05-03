import pandas as pd

data = pd.read_csv('./data/places.txt',sep='hhh',engine='python',header=None)
with open('./data/new_places.txt','w') as f:
    for i in data[0]:
        f.write(i)
        f.write(' ')
        f.write('ns')
        f.write('\n')