# coding:utf-8
import re,time
from datetime import datetime,timedelta
#返回当前时间，以字符串形式
def file_date():
    return str(datetime.now()).split()[0]+'/'

# 返回指定天数前的日期
def get_date(days=7):
    return datetime.now() - timedelta(days=days)
# 将采集字段中的字符串转换成指定格式的时间 "%Y-%m-%d"
def convert_time(collect_date,name):
    if name=="ccgp":
        mat = re.findall(r"(\d*)", collect_date)
        mat = mat[0] + '-' + mat[2] + '-' + mat[4]
    else:
        mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", collect_date).group()
    return  datetime.strptime(mat, "%Y-%m-%d")
def utc_timestamp():
    """返回utc时间戳（秒）"""
    return int(datetime.now().timestamp())
# 将时间戳转换成秒
def convert_seconds(time1,time2):
    seconds=time.localtime(time2-time1)
    return seconds.tm_sec
