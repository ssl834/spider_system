# coding:utf-8


import requests
import chardet
from src.proxy_server.proxy_config import get_header,TIMEOUT,RETRY_TIME
from src.proxy_server.proxy_config import PROXY_CONF


class Html_Downloader(object):
    @staticmethod
    def download(url,proxy_type):
        # 从代理网站下载ip
        count=0
        while count<RETRY_TIME:
            # 如果是免费ip
            if proxy_type=='free':
                r=requests.get(url=url,headers=get_header(),timeout=TIMEOUT)
                r.encoding = chardet.detect(r.content)['encoding']
                if (not r.ok) or len(r.content) < 500:
                    count+=1
                else:
                    return r.text
            # 如果是付费ip,则进行请求时可能需要携带cookie
            elif proxy_type=='pay':
                r = requests.get(url=url, headers=get_header(),cookie=PROXY_CONF['proxy_type'][proxy_type]['cookies'], timeout=TIMEOUT)
                if (not r.ok) or len(r.content) < 500:
                    count += 1
                else:
                    return r.text
            else:
                return

