import requests
from ..config import RETYE_TIME,SPIDER_CONF
from src.snatch_server.commons.get_proxy import get_proxy
from src.snatch_server.commons.get_headers import get_header
from src.proxy_server.get_del_proxy import ProxyOperate
class HtmlDownLoad(object):
    def down_load(self,url,spider_name,cookies=None):

        headers=get_header()
        count=0
        # 重试次数
        while count<RETYE_TIME:
            try:
                if SPIDER_CONF[spider_name]['is_proxy']:
                    proxy = get_proxy(spider_name)
                    if cookies:
                        resp = requests.get(url=url, headers=headers, cookies=cookies, proxies=proxy, timeout=5)
                    else:
                        resp = requests.get(url=url, headers=headers, proxies=proxy, timeout=5)
                elif cookies:
                    resp=requests.get(url=url,headers=headers,cookies=cookies)
                else:
                    resp=requests.get(url=url, headers=headers,timeout=5)
                if resp.status_code==200:
                    # 将相应解码，防止乱码
                    resp.encoding = resp.apparent_encoding

                    return resp
                else:
                    # 调用函数将此proxy删除
                    count += 1
                    try:
                        ProxyOperate().del_proxy(spider_name,proxy)
                    except:
                        pass
            except:
                count += 1
                try:
                    ProxyOperate().del_proxy(spider_name, proxy)
                except:
                    pass
        return

