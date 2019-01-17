from ..config import SPIDER_CONF
from urllib import parse
# 获取对应的爬虫搜索关键字
def get_kws(spider_name):
    key_words=SPIDER_CONF[spider_name]['kws']
    return [parse.quote(kw) for kw in key_words]