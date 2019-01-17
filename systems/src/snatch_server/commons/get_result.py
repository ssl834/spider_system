#coding=utf-8
from src.snatch_server.config import SPIDER_CONF
import time
from src.snatch_server.db.DataStore import get_sqlhelper
from src.snatch_server.utils.send_mail import SendEmail
# 获取抓取结果 邮件通知
def get_spider_result(*args):
    results={}
    for i in args:
        sqlhelper=get_sqlhelper(i)
        nums=sqlhelper.get_total()
        results[i]=nums
    content=''
    for k,v in results.items():
        if v:
            content+='{}已经抓取完成,共抓取{}条数据\n'.format(k,v)
        else:
            content += '{}已经抓取完成,共抓取{}条数据,数据异常，请处理\n'.format(k, v)
    title='spider完成通知'
    try:
        SendEmail().send_email(title,content)
    except:
        time.sleep(5*60)
        SendEmail().send_email(title, content)


