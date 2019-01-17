#coding=utf-8

import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(os.path.split(rootPath)[0])
from multiprocessing import Process

from src.proxy_server.validator.Validator import Verificate
from src.proxy_server.spider.ProxyCrawl import startProxyCrawl
from src.snatch_server.utils.get_proxy_type import get_proxy_type
def main(proxy_type):
    p1 = Process(target=startProxyCrawl, args=(proxy_type,))
    p2 = Process(target=Verificate(proxy_type).re_verificate, args=(proxy_type,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
def proxy_run():
    for i in get_proxy_type():
        main(i)
if __name__ == '__main__':
    proxy_run()
