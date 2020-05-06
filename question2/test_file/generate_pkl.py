import pickle

import pandas as pd

changsha_ns = pd.read_csv('//question2/data/changsha_ns.txt',
                          engine='python')
new_places_ns = pd.read_csv('//question2/data/places.txt', sep=' ',
                            engine='python')
data = list(changsha_ns)
pickle.dump(str(data[0]), open('//question2/data/changsha_ns.pkl', 'w'))
