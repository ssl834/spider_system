# coding:utf-8
import sys


from ..config import SPIDER_CONF
def get_sqlhelper(spider_name):
    try:

        if SPIDER_CONF[spider_name]['db_type'] == 'mongo':
            from ..db.MongoHelper import MongoHelper as SqlHelper
        else:
            from ..db.RedisHelper import RedisHelper as SqlHelper
        sqlhelper = SqlHelper(spider_name)
        #数据库初始化
        try:
            sqlhelper.init_db()
        except:
            pass
        return sqlhelper
    except Exception as e:
        raise BaseException


