import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))

rootPath = os.path.split(curPath)[0]

sys.path.append(os.path.split(rootPath)[0])
