# coding:utf-8
from __future__ import unicode_literals

from redis import Redis

from proxy_server.config import PROXY_CONF
from proxy_server.db.ISqlHelper import ISqlHelper
from proxy_server.db.SqlHelper import Proxy


class RedisHelper(ISqlHelper):
    def __init__(self,proxy_type):
        self.proxy_type=proxy_type
        self.index_names = ('proxy_type',)
        self.redis_url = PROXY_CONF['proxy_type'][self.proxy_type]['db_connection']

    def get_proxy_name(self, ip=None, port=None, proxy=None):
        ip = ip or proxy.ip
        port = port or proxy.port

        return "proxy::{}:{}".format(ip, port)

    def get_index_name(self, index_name, value=None):
        if index_name == 'proxy_type':
            return 'index::proxy_type'
        return "index::{}:{}".format(index_name, value)

    def get_proxy_by_name(self, name):
        pd = self.redis.hgetall(name)
        if pd:
            return Proxy(**{k.decode('utf8'): v.decode('utf8') for k, v in pd.items()})

    def init_db(self):
        self.redis = Redis.from_url(self.redis_url)

    def drop_db(self):
        return self.redis.flushdb()

    def get_keys(self, conditions):
        select_keys = {self.get_index_name(key, conditions[key]) for key in conditions.keys() if
                       key in self.index_names}
        if 'ip' in conditions and 'port' in conditions:
            return self.redis.keys(self.get_proxy_name(conditions['ip'], conditions['port']))
        if select_keys:
            return [name.decode('utf8') for name in self.redis.sinter(keys=select_keys)]
        return []

    def insert(self, value):
        proxy = Proxy(ip=value['ip'], port=value['port'],

                      speed=value['speed'])
        mapping = proxy.__dict__
        for k in list(mapping.keys()):
            if k.startswith('_'):
                mapping.pop(k)
        object_name = self.get_proxy_name(proxy=proxy)
        # 存结构
        insert_num = self.redis.hmset(object_name, mapping)
        # 创建索引
        if insert_num > 0:
            for index_name in self.index_names:
                self.create_index(index_name, object_name, proxy)
        return insert_num

    def create_index(self, index_name, object_name, proxy):
        redis_key = self.get_index_name(index_name, getattr(proxy, index_name))
        return self.redis.sadd(redis_key, object_name)
    def get_total(self):
        total=self.redis.keys(self.get_proxy_by_name(self.proxy_type)).count()
        return total
    def delete(self, conditions=None):
        proxy_keys = self.get_keys(conditions)
        index_keys = self.redis.keys(u"index::*")
        if not proxy_keys:
            return 0

        for iname in index_keys:
            self.redis.srem(iname, *proxy_keys)
        return self.redis.delete(*proxy_keys) if proxy_keys else 0


    def select(self, count=None, conditions=None):
        count = (count and int(count)) or 1000  # 最多返回1000条数据
        count = 1000 if count > 1000 else count

        querys = {k: v for k, v in conditions.items() if k in self.index_names} if conditions else None

        objects = list(self.get_keys(querys))[:count]
        redis_name = self.get_index_name(self.proxy_type)
        objects.sort(key=lambda x: int(self.redis.zscore(redis_name, x)))

        result = []
        for name in objects:
            p = self.get_proxy_by_name(name)
            result.append((p.ip, p.port))
        return result


