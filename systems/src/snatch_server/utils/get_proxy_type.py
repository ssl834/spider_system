from src.snatch_server.config import SPIDER_CONF
def get_proxy_type():
    l=[]
    for k,v in SPIDER_CONF.items():
        if v['is_proxy']:
            l.append(v['proxy_type'])
    return list(set(l))