# coding:utf-8
import base64


import re



from lxml import etree


class Html_Parser(object):


    def parse(self, response, parser):
        '''

        :param response: 响应
        :param type: 解析方式
        :return:
        '''
        if parser['type'] == 'xpath':
            return self.XpathPraser(response, parser)
        elif parser['type'] == 'regular':
            return self.RegularPraser(response, parser)
        elif parser['type'] == 'module':
            return getattr(self, parser['moduleName'], None)(response, parser)
        else:
            return None



    def XpathPraser(self, response, parser):
        '''
        针对xpath方式进行解析
        :param response:
        :param parser:
        :return:
        '''
        proxylist = []
        root = etree.HTML(response)
        proxys = root.xpath(parser['pattern'])
        for proxy in proxys:
            try:
                ip = proxy.xpath(parser['position']['ip'])[0].text
                port = proxy.xpath(parser['position']['port'])[0].text
                type = 0
                protocol = 0

            except Exception as e:
                continue

            proxy = {'ip': ip, 'port': int(port), 'types': int(type), 'protocol': int(protocol), 'speed': 100}
            proxylist.append(proxy)
        return proxylist

    def RegularPraser(self, response, parser):
        '''
        针对正则表达式进行解析
        :param response:
        :param parser:
        :return:
        '''
        proxylist = []
        pattern = re.compile(parser['pattern'])
        matchs = pattern.findall(response)
        if matchs != None:
            for match in matchs:
                try:
                    ip = match[parser['position']['ip']]
                    port = match[parser['position']['port']]
                    # 网站的类型一直不靠谱所以还是默认，之后会检测
                    type = 0
                    protocol = 0
                except Exception as e:
                    continue

                proxy = {'ip': ip, 'port': port, 'types': type, 'protocol': protocol, 'country': country, 'area': area,
                         'speed': 100}

                proxylist.append(proxy)
            return proxylist


    def CnproxyPraser(self, response, parser):
        proxylist = self.RegularPraser(response, parser)
        chardict = {'v': '3', 'm': '4', 'a': '2', 'l': '9', 'q': '0', 'b': '5', 'i': '7', 'w': '6', 'r': '8', 'c': '1'}

        for proxy in proxylist:
            port = proxy['port']
            new_port = ''
            for i in range(len(port)):
                if port[i] != '+':
                    new_port += chardict[port[i]]
            new_port = int(new_port)
            proxy['port'] = new_port
        return proxylist


    def proxy_listPraser(self, response, parser):
        proxylist = []
        pattern = re.compile(parser['pattern'])
        matchs = pattern.findall(response)
        if matchs:
            for match in matchs:
                try:
                    ip_port = base64.b64decode(match.replace("Proxy('", "").replace("')", ""))
                    ip = ip_port.split(':')[0]
                    port = ip_port.split(':')[1]
                    type = 0
                    protocol = 0

                except Exception as e:
                    continue
                proxy = {'ip': ip, 'port': int(port), 'types': type, 'protocol': protocol, 'speed': 100}
                proxylist.append(proxy)
            return proxylist







