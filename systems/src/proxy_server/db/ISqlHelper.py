# coding:utf-8

class ISqlHelper(object):
    params = {'ip': None, 'port': None,'proxy_type':None}

    def init_db(self):
        raise NotImplemented

    def drop_db(self):
        raise NotImplemented

    def insert(self, value):
        raise NotImplemented

    def delete(self, conditions=None):
        raise NotImplemented

    def select(self, count=None, conditions=None):
        raise NotImplemented
    def get_total(self):
        raise NotImplemented