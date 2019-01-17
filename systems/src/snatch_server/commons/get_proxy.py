#coding:utf-8
import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))

rootPath = os.path.split(curPath)[0]

sys.path.append(os.path.split(rootPath)[0])



from src.proxy_server.get_del_proxy import ProxyOperate
from src.proxy_server.validator.Validator import Verificate
from ..config import SPIDER_CONF
import time,sys
#获取代理
def get_proxy(spider_name):
    # 代理类型
    proxy_type=SPIDER_CONF[spider_name]['proxy_type']
    proxy=ProxyOperate().get_proxy(proxy_type)
    if isinstance(proxy,dict):

        pro = proxy['http'].split(':')
        ip = pro[1]
        port = int(pro[2])
        result=Verificate(proxy_type).checkout(ip,port)

    else:
        result=None

    if result is not None:

        return proxy
    else:
        time.sleep(5)
        #代理验证不合格，再次获取
        str="--->>>>>Proxy is not useful,try again,please wait.....\n"
        sys.stdout.write(str)
        sys.stdout.flush()
        get_proxy(spider_name)
