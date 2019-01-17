# coding:utf-8

class ISqlHelper(object):


    def init_db(self):
        raise NotImplemented

    def drop_db(self):
        raise NotImplemented

    def insert(self, value):
        raise NotImplemented

    def delete(self, conditions=None):
        raise NotImplemented
