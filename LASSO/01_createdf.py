import os, glob
from Cleaner import *


cwd = os.getcwd()
par0 = os.path.abspath(os.path.join(cwd, os.pardir))
par = os.path.abspath(os.path.join(par0, os.pardir))
src = os.path.join(par, 'Sources')
#zero_path = os.path.join(src, 'neutral')
#one_path = os.path.join(src, 'racist')

D = []
for path, subdirs, files in os.walk(src):
    for name in files:
        v = 0
        if 'racist' in path:
            v=1
        D.append([os.path.join(path, name),v])
print(D)
#stem each book and create dictionary
