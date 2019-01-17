# coding:utf-8
import time,random,sys
from src.snatch_server.config import SPIDER_CONF
from src.proxy_server.db.DataStore import get_sqlhelper
from src.snatch_server.utils.time_utils import convert_seconds
from src.snatch_server.config import ALARM_TIME
from src.snatch_server.utils.send_mail import SendEmail
class ProxyOperate(object):
    """操作代理"""
    # 随机获得代理
    now=time.time()
    flag=1
    def get_proxy(self,proxy_type):
        sqlhelper = get_sqlhelper(proxy_type)
        proxy = sqlhelper.select()
        if proxy:
            proxy = random.sample(proxy, 1)
            proxy_dict = {
                'http': 'http:{}:{}'.format(proxy[0][0], proxy[0][1]),
                'https': 'http:{}:{}'.format(proxy[0][0], proxy[0][1])
            }
            return proxy_dict
        else:
            str = "Acquiring Proxies Now，Please Wait For A Little Time--->>>>>>"
            sys.stdout.write(str + '\r\n')
            sys.stdout.flush()
            stop_time=time.time()
            # 如果超出设置的报警时间 则发送邮件通知管理员 进行处理
            if convert_seconds(self.now,stop_time) > ALARM_TIME and self.flag:
                SendEmail().send_email('代理警报','超出设定时间，无可用代理，请处理')
                self.flag=0
            time.sleep(2)
            self.get_proxy(proxy_type)
    # 将不符合使用的代理删除
    def del_proxy(self,name,proxies):
        if isinstance(proxies,dict):
            proxy_type=SPIDER_CONF[name]['proxy_type']
            sqlhelper = get_sqlhelper(proxy_type)
            pro=proxies['http'].split(':')
            ip=pro[1]
            port=int(pro[2])
            sqlhelper.delete({'ip':ip,'port':port})
if __name__ == "__main__":
    ProxyOperate().get_proxy('free')

