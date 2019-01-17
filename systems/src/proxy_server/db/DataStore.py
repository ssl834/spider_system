# coding:utf-8
import sys


from ..proxy_config import PROXY_CONF
def get_sqlhelper(db_name):
    try:
        #专用代理存储MongoDB
        if db_name == 'free':
            from src.proxy_server.db.MongoHelper import MongoHelper as SqlHelper
        else:
            #免费和专用则存储在redis
            # from db.RedisHelper import RedisHelper as SqlHelper
            from src.proxy_server.db.RedisHelper import RedisHelper as SqlHelper
        sqlhelper = SqlHelper(db_name)
        #数据库初始化
        try:
            sqlhelper.init_db()
        except:
            pass
        return sqlhelper
    except Exception as e:
        raise BaseException


