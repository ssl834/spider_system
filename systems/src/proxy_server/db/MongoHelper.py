import pymongo
from src.proxy_server.proxy_config import PROXY_CONF

from src.proxy_server.db.ISqlHelper import ISqlHelper


class MongoHelper(ISqlHelper):
    def __init__(self,proxy_type):
        self.proxy_type = proxy_type
        self.client = pymongo.MongoClient(PROXY_CONF['proxy_type'][self.proxy_type]['db_connection'], connect=False)

    def init_db(self):
        self.db = self.client.proxy
        self.proxys = self.db.proxys

    def drop_db(self):
        self.client.drop_database(self.db)

    def insert(self, value=None):
        if value:
            proxy = dict(ip=value['ip'], port=value['port'],
                        speed=value['speed'],proxy_type=self.proxy_type)
            self.proxys.insert(proxy)

    def delete(self, conditions=None):
        if conditions:
            self.proxys.remove(conditions)
            return ('deleteNum', 'ok')
        else:
            return ('deleteNum', 'None')

    def get_total(self):
        total=self.proxys.find({'proxy_type':self.proxy_type}).count()
        return total


    def select(self, count=None, conditions=None):
        if count:
            count = int(count)
        else:
            count = 0
        if conditions:
            conditions = dict(conditions)

            conditions_name = ['types', 'protocol']
            for condition_name in conditions_name:
                value = conditions.get(condition_name, None)
                if value:
                    conditions[condition_name] = int(value)
        else:
            conditions = {}
        items = self.proxys.find(conditions, limit=count).sort(
            [("speed", pymongo.ASCENDING)])
        results = []
        for item in items:
            result = (item['ip'], item['port'])
            results.append(result)
        return results
