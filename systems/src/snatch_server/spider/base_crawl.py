import random, time, os
from ..config import SPIDER_CONF,DEFAULT_PAGE
from ..commons.html_down_load import HtmlDownLoad
from ..commons.html_parse import HtmlParse
from ..utils.zstd import ZstdUtils
from ..utils.file_utils import write_files
from ..utils.time_utils import file_date, utc_timestamp
from ..utils.file_path_format import makedir
from ..db.DataStore import get_sqlhelper
from ..commons.get_proxy import get_proxy

class BaseCrawl(object):
    # 默认的爬虫name
    name = None
    # 页数
    pageNo = 1
    # 停止标志,0时停止
    stop_flag = 1
    # 搜索时关键字
    kws = []
    # 来源
    source_from = name
    # 版本
    version = '2.0'
    # 时间戳
    update_time = utc_timestamp
    # 当前时间
    file_date = file_date()
    # 其实url
    url = ''
    # 没有获得响应时默认抓取页数
    default_pageNo=DEFAULT_PAGE
    def __init__(self):
        self.html_down = HtmlDownLoad()
        self.html_parse = HtmlParse()

    def start_crawl(self):
        for kw in self.kws:
            while self.stop_flag:
                url = self.url.format(str(self.pageNo), kw)
                time.sleep(random.randrange(5))
                self.get_url(url)
                self.pageNo += 1
            self.stop_flag=1
            self.pageNo=1
    def get_url(self, url):
        # 获得响应

        if SPIDER_CONF[self.name]['is_proxy']:
            proxy=get_proxy(self.name)
            resp = self.html_down.down_load(url,self.name)
        else:
            resp = self.html_down.down_load(url,self.name)
        if resp:
            #     解析
            urls = self.html_parse.html_parse_url(resp, self.name)

            if urls:
                time.sleep(random.randrange(5))
                for url in urls:
                    self.get_detail(url)
            else:
                self.stop_flag = 0
                self.pageNo = 1
        else:
            if self.pageNo>self.default_pageNo:
                self.stop_flag = 0
                self.pageNo = 1

    def get_detail(self, url):
        resp = self.html_down.down_load(url,self.name)
        if resp:
            # 存储数据
            items = self.html_parse.html_parse_content(resp, self.name)
            items['url'] = resp.url
            items['source_from'] = self.source_from
            # items['update_time'] = self.update_time
            items['version'] = self.version
            if SPIDER_CONF[self.name]['store_html']:
                items['htm_src'] = ZstdUtils(level=1).compress(resp.text)
            # 存储到对应的数据库中
            sqlhelper = get_sqlhelper(self.name)
            sqlhelper.insert(items)
            current_file_path = os.path.dirname(os.path.dirname(__file__))
            directory = '//scrapy_datas//{}//'.format(self.name)
            # 保存文件后缀
            suffix = '.html'
            pa = current_file_path + directory + self.file_date
            makedir(pa)
            path = current_file_path + directory + self.file_date + items.get('title') + suffix
            write_files(path, resp.text)
            if self.stop_sign(items):
                self.stop_flag = 0
                self.pageNo = 1

    def stop_sign(self, items):
        """终止标志"""

        pass
