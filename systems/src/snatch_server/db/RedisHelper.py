# coding:utf-8

import json
from redis import Redis
from ..config import SPIDER_CONF

from ..db.ISqlHelper import ISqlHelper

class RedisHelper(ISqlHelper):
    def __init__(self,spider_name):
        self.spider_name=spider_name
        self.db_name=SPIDER_CONF[spider_name]['db_name']
        self.redis_url = SPIDER_CONF[spider_name]['db_connection']


    def init_db(self):
        self.redis = Redis.from_url(self.redis_url)

    def drop_db(self):
        return self.redis.flushdb()

    def insert(self, value):
        if isinstance(value,dict):
            insert_num=self.redis.set(json.dumps(value),self.spider_name)
            return insert_num

    def delete(self, conditions=None):
        keys_list=self.redis.keys()
        for i in keys_list:
            # 转换成字典
            j=json.loads(i)
            if set(conditions.items()).issubset(j.items()):
                self.redis.delete(i)
    def select(self,conditions=None):
        keys_list = self.redis.keys()
        for i in keys_list:
            # 转换成字典
            j = json.loads(i)
            if self.redis.get(i)==self.spider_name:
                if set(conditions.items()).issubset(j.items()):
                    return j
    def get_total(self):
        return self.redis.keys().count()













