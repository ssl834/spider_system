#coding:utf-8
# 获得path中的/进行去除
import os
def makedir(path):
    path = path.strip()
    path=path.rstrip('//')
    is_exist=os.path.exists(path)
    if not is_exist:
        os.makedirs(path)

