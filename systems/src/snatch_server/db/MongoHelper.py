import pymongo
from ..config import SPIDER_CONF

from ..db.ISqlHelper import ISqlHelper


class MongoHelper(ISqlHelper):
    def __init__(self,spider_name):
        self.spider_name=spider_name
        self.db_name=SPIDER_CONF[spider_name]['db_name']
        conection = SPIDER_CONF[spider_name]['db_connection']
        self.client = pymongo.MongoClient(conection)

    def init_db(self):
        # 默认集合名为爬虫名
        self.db = self.client[self.db_name]
        self.col =self.db[ SPIDER_CONF[self.spider_name]['col_name']]

    def drop_db(self):
        self.client.drop_database(self.db)

    def insert(self, value=None):
        if value:
            if not self.col.find_one(value):
                self.col.insert(value)

    def delete(self, conditions=None):
        if conditions:
            self.col.remove(conditions)
            return ('deleteNum', 'ok')
        else:
            return ('deleteNum', 'None')
    def select(self,conditions=None):
        if conditions:
            return [dict(i) for i in self.col.find(conditions)]
    def get_total(self):

        total=self.col.find({'source_from':self.spider_name}).count()

        return total
