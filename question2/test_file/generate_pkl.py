import pandas as pd
import pickle

changsha_ns = pd.read_csv('/home/asimov/PycharmProjects/question_2/question2/data/changsha_ns.txt',
                          engine='python')
new_places_ns = pd.read_csv('/home/asimov/PycharmProjects/question_2/question2/data/new_places.txt', sep=' ',
                            engine='python')
data= list(changsha_ns)
pickle.dump(str(data[0]), open('/home/asimov/PycharmProjects/question_2/question2/data/changsha_ns.pkl', 'w'))
