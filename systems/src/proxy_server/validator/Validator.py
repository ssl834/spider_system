#coding=utf-8
import os,sys

import gevent

import chardet
import requests,time
from src.proxy_server.proxy_config import get_header,PROXY_CONF,TIMEOUT
from src.proxy_server.db.DataStore import get_sqlhelper
import psutil
from multiprocessing import Process, Queue
class Verificate(object):
    def __init__(self,proxy_type):
        self.proxy_type=proxy_type
        self.headers=get_header()
        self.url='http:www.baidu.com'
        self.proc_pool = {}  # 所有进程列表
        self.cntl_q = Queue()
    def checkout(self,host,port):
        proxy_url = '{}:{}'.format(host, port)
        proxies = {
            'http': proxy_url,
            'https': proxy_url
        }
        start = time.time()
        try:
            r = requests.get(url='https://www.baidu.com', headers=get_header(), timeout=TIMEOUT,
                             proxies=proxies)
            r.encoding = chardet.detect(r.content)['encoding']

            if r.ok:
                speed = round(time.time() - start, 2)
                return speed
            else:
                sqlhelper = get_sqlhelper(self.proxy_type)
                try:
                    sqlhelper.delete({'ip': host, 'port': port})
                except:
                    pass
        except:
            sqlhelper = get_sqlhelper(self.proxy_type)
            try:
                sqlhelper.delete({'ip': host, 'port': port})
            except:
                pass



    #自我检测
    def re_verificate(self,proxy_type):
        sqlhelper = get_sqlhelper(proxy_type)
        proxy_list=sqlhelper.select()
          # 所有进程列表
         # 控制信息队列
        str = ">>>>>>>>Verificating Proxies Now,Please Ignor This Message>>>>>>>>>>\n"
        sys.stdout.write(str)
        sys.stdout.flush()
        while 1:

            if not proxy_list:
                time.sleep(5)
            if not self.cntl_q.empty():
                # 处理已结束的进程
                try:
                    pid = self.cntl_q.get()
                    proc = self.proc_pool.pop(pid)
                    proc_ps = psutil.Process(pid)
                    proc_ps.kill()
                    proc_ps.wait()
                except Exception as e:
                    pass
            while 1:
                if len(self.proc_pool) >= PROXY_CONF['proxy_type'][self.proxy_type]['max_check_process_num']:
                    time.sleep(PROXY_CONF['proxy_type'][self.proxy_type]['check_wait_time'])

                    continue
                else:
                    p = Process(target=self.process_start,args=(proxy_list,))
                    p.start()
                    self.proc_pool[p.pid] = p
                    break

    def process_start(self,proxy_list):
        spawns = []
        for task in proxy_list:
            spawns.append(gevent.spawn(self.checkout,task[0],task[1]))
        gevent.joinall(spawns)
        self.cntl_q.put(os.getpid())  # 子进程退出是加入控制队列
