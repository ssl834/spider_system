import re
from lxml import etree
from lxml.etree import _Element

from ..config import SPIDER_CONF
from ..utils.file_utils import format_file
class HtmlParse(object):
    def html_parse_url(self,response,spider_name):
        parse_method=SPIDER_CONF[spider_name]['url_parse']['parse_type']
        if parse_method=='xpath':
            pattern=SPIDER_CONF[spider_name]['url_parse']['pattern']
            results=self.xpath_method(response,pattern)
            return results
        return []
    def html_parse_content(self,response,spider_name):
        pattern= SPIDER_CONF[spider_name]['content_parse']['pattern']
        results={}

        for k,v in pattern.items():
            # xpath解析
            if v[0]=='xpath':
                res=self.xpath_method(response,v)
                results[k]=res
            # 正则解析
            elif v[0]=='re':
                res=self.re_method(response,v)
                results[k]=res
            #     第三方解析
            else:
                res=self.third_method(response,v)
                results[k] = res
        if spider_name=='jincai':
            pub=results.get('public_time')[5:]
            results['public_time']=pub
        return results
    # xpath解析
    def xpath_method(self,response,pattern):
        html=etree.HTML(response.text)
        if len(pattern)==1:
            results=html.xpath(pattern[0])
        else:
            try:
                results=html.xpath(pattern[1])[pattern[2]]
            except:
                results=''
        return results
    # 正则解析
    def re_method(self,response,pattern):
        try:
            res=re.findall(pattern[1],response.text)[pattern[2]][pattern[3]:]
        except:
            res=''
        return res
    # 第三方解析,主要文本内容需要进行处理
    def third_method(self,response,pattern):
        html=etree.HTML(response.text)
        res=''
        for i in pattern[1]:
            content=html.xpath(i)
            try:
                res+=format_file(content, filtrate=' ')
            except TypeError:
                content=self.getText(content[0])
                res+='\n公告正文\n'
                res+=format_file(content, filtrate=' ')
        return res
    # 解析某一块下面的所有内容
    def getText(self,elem):
        rc = []
        for node in elem.itertext():
            rc.append(node.strip())
        return ''.join(rc)



