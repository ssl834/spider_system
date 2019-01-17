#coding=utf-8

import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.split(curPath)[0])

from src.snatch_server.commons.get_result import get_spider_result
from src.snatch_server.spider.spider_list import CrawlZ,CrawlC,CrawlJ
from multiprocessing import Process

j=CrawlJ()
c=CrawlC()
z=CrawlZ()



if __name__ == '__main__':
    p1=Process(target=j.start_crawl())
    p2=Process(target=c.start_crawl())
    p3=Process(target=z.start_crawl())
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
    str='>>>>>>>Crawl Over!Please Touch Your Email And To see The Result>>>>>>>'
    sys.stdout.write(str + '\r\n')
    sys.stdout.flush()
    get_spider_result(z.name)


