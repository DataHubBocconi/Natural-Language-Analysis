import os, glob
import pandas as pd
from Cleaner import *
from collections import defaultdict



cwd = os.getcwd()
par0 = os.path.abspath(os.path.join(cwd, os.pardir))
par = os.path.abspath(os.path.join(par0, os.pardir))
src = os.path.join(par, 'Sources')
#zero_path = os.path.join(src, 'neutral')
#one_path = os.path.join(src, 'racist')

oD = []
for path, subdirs, files in os.walk(src):
    for name in files:
        v = 0
        if 'racist' in path:
            v=1
        oD.append([os.path.join(path, name),v,name])
#stem each book and create dictionary
D = []
for d in oD:
    D.append([clean_book(d[0]), d[1],d[2]])
C = []
for d in D:
    C.append({})
    for w in d[0]:
        try:
            C[-1][w] += 1
        except KeyError:
            C[-1][w] = 1
    C[-1]['racist'] = d[1]
    C[-1]['name'] = d[2]

df = pd.DataFrame(C)
print(df.head())
df.fillna(0, inplace=True)
print(df.head())
df.to_csv(os.path.join(par, 'Data','rawdata.csv'))