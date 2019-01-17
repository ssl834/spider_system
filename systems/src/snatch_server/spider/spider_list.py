from .base_crawl import BaseCrawl
from ..utils.get_kws import get_kws
from ..commons.get_proxy import get_proxy
from ..utils.time_utils import convert_time,get_date
from ..config import SPIDER_CONF
class CrawlZ(BaseCrawl):
    """中国招标与采购"""
    name='zbytb'
    kws = get_kws(name)
    url= 'http://www.zbytb.com/zb/search.php?page={}&kw={}'
    source_from=name
    def stop_sign(self, items):
        public_time = items['public_time']
        public_time = convert_time(public_time, self.name)
        items['public_time'] = public_time
        if items['public_time'] < get_date(7):
            return True
class CrawlC(BaseCrawl):
    """中国政府采购网"""
    url = 'http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index={}&kw={}'
    name='ccgp'
    kws=get_kws(name)
    source_from = name

    def stop_sign(self, items):
        public_time = items['public_time']
        public_time = convert_time(public_time, self.name)
        items['public_time'] = public_time
        if items['public_time'] < get_date(7):
            return True
class CrawlJ(BaseCrawl):
    """金采网"""
    url = 'http://www.cfcpn.com/plist/caigou?pageNo={}&kflag=0&keyword={}&keywordType=&province=&city=&typeOne=&ptpTwo=,,,,,'
    name = 'jincai'
    kws = get_kws(name)
    source_from = name
    # 进行添加前缀
    def get_url(self, url):
        # 获得响应
        resp = self.html_down.down_load(url,self.name)
        if resp:
            #     解析
            urls = self.html_parse.html_parse_url(resp, self.name)
            if urls:
                url_prefix = r'http://www.cfcpn.com'
                for url in urls:
                    self.get_detail(url_prefix+url)
            else:
                self.stop_flag = 0
                self.pageNo = 1
        else:
            if self.pageNo>self.default_pageNo:
                self.stop_flag = 0
                self.pageNo = 1

    def stop_sign(self, items):
        public_time = items['public_time']
        public_time = convert_time(public_time, self.name)

        if public_time < get_date(7):
            return True