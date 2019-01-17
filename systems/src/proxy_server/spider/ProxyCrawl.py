# coding:utf-8




import sys
import time
import gevent

from gevent.pool import Pool
from multiprocessing import Queue
from src.proxy_server.db.DataStore import get_sqlhelper
from src.proxy_server.spider.HtmlDownloader import Html_Downloader
from src.proxy_server.spider.HtmlPraser import Html_Parser
from src.proxy_server.validator.Validator import Verificate
from src.proxy_server.proxy_config import PROXY_CONF, TASK_QUEUE_SIZE


# 开启采集程序
def startProxyCrawl(proxy_type):
    crawl = ProxyCrawl(proxy_type)
    crawl.run()


class ProxyCrawl(object):
    """爬虫主程序"""
    proxies = set()

    def __init__(self, proxy_type):
        self.crawl_pool = Pool(PROXY_CONF['proxy_type'][proxy_type]['thread_num'])
        self.queue = Queue(maxsize=TASK_QUEUE_SIZE)
        self.proxy_type = proxy_type

    def run(self):
        while True:
            sqlhelper = get_sqlhelper(self.proxy_type)
            gather_count = sqlhelper.get_total()
            if gather_count < PROXY_CONF['proxy_type'][self.proxy_type]['min_num']:
                str = "----->>>>>>ProxyPool starting"
                sys.stdout.write(str + '\r\n')
                sys.stdout.flush()
                #ip数量不足，开始采集数据
                target_list = PROXY_CONF['proxy_type'][self.proxy_type]['parse_list']

                spawns = []
                for proxy in target_list:
                    spawns.append(gevent.spawn(self.crawl, proxy))
                    # 如果协程数超过设置数值
                    if len(spawns) >= PROXY_CONF['proxy_type'][self.proxy_type]['max_download_num']:
                        gevent.joinall(spawns)
                        spawns = []
                gevent.joinall(spawns)

            else:
                str = '\r\nIPProxyPool----->>>>>>>>now ip num meet the requirement,wait UPDATE_TIME...'
                sys.stdout.write(str + "\r\n")
                sys.stdout.flush()

                time.sleep(PROXY_CONF['proxy_type'][self.proxy_type]['update_time'])

    def crawl(self, parser):
        sqlhelper = get_sqlhelper(self.proxy_type)
        if self.proxy_type != 'dedicated':
            html_parser = Html_Parser()

            for url in parser['urls']:

                response = Html_Downloader.download(url, self.proxy_type)
                if response is not None:
                    proxylist = html_parser.parse(response, parser)
                    if proxylist is not None:

                        for proxy in proxylist:

                            result = Verificate(self.proxy_type).checkout(proxy['ip'], proxy['port'])
                            if result is not None:
                                str = '\r\n----->>>>>>>> ip is useful'
                                sys.stdout.write(str + "\r\n")
                                sys.stdout.flush()
                                proxy['speed'] = result
                                sqlhelper.insert(proxy)

                            while 1:
                                sqlhelper = get_sqlhelper(self.proxy_type)
                                count = sqlhelper.get_total()

                                if count>PROXY_CONF['proxy_type'][self.proxy_type]['min_num']:
                                    str = '\r\nIPProxyPool----->>>>>>>>now ip num meet the requirement,wait UPDATE_TIME...'
                                    sys.stdout.write(str + "\r\n")
                                    sys.stdout.flush()
                                    time.sleep(PROXY_CONF['proxy_type'][self.proxy_type]['update_time'])
                                else:
                                    break
        else:
            for proxy in PROXY_CONF['proxy_type'][self.proxy_type]['parse_list']:
                result = Verificate(self.proxy_type).checkout(proxy['ip'], proxy['port'])
                if result:
                    proxy['speed'] = result
                    sqlhelper.insert(proxy)
