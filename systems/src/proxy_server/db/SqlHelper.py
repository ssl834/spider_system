# coding:utf-8
import datetime
from sqlalchemy import Column, Integer,  DateTime, Numeric, create_engine, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.proxy_server.proxy_config import PROXY_CONF
from src.proxy_server.db.ISqlHelper import ISqlHelper



BaseModel = declarative_base()


class Proxy(BaseModel):
    __tablename__ = 'proxys'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(VARCHAR(16), nullable=False)
    port = Column(Integer, nullable=False)
    proxy_type = Column(VARCHAR(16), nullable=False, default='')
    updatetime = Column(DateTime(), default=datetime.datetime.utcnow)
    speed = Column(Numeric(5, 2), nullable=False)


class SqlHelper(ISqlHelper):
    params = {'ip': Proxy.ip, 'port': Proxy.port, 'proxy_type': Proxy.proxy_type}

    def __init__(self, proxy_type):
        self.proxy_type = proxy_type
        self.engine = create_engine(PROXY_CONF['proxy_type'][self.proxy_type]['db_connection'], echo=False)
        DB_Session = sessionmaker(bind=self.engine)
        self.session = DB_Session()

    def init_db(self):
        BaseModel.metadata.create_all(self.engine)

    def drop_db(self):
        BaseModel.metadata.drop_all(self.engine)

    def insert(self, value):
        proxy = Proxy(ip=value['ip'], port=value['port'],
                      speed=value['speed'], proxy_type=self.proxy_type)
        self.session.add(proxy)
        self.session.commit()

    def get_total(self):
        query = self.session.query(Proxy)
        total = query.filter(Proxy.proxy_type == self.proxy_type).count()

        return total

    def delete(self, conditions=None):
        if conditions:
            conditon_list = []
            for key in list(conditions.keys()):
                if self.params.get(key, None):
                    conditon_list.append(self.params.get(key) == conditions.get(key))
            conditions = conditon_list
            query = self.session.query(Proxy)
            for condition in conditions:
                query = query.filter(condition)
            deleteNum = query.delete()
            self.session.commit()
        else:
            deleteNum = 0
        return ('deleteNum', deleteNum)

    def select(self, count=None, conditions=None):
        '''
        conditions的格式是个字典。类似self.params
        :param count:
        :param conditions:
        :return:
        '''
        if conditions:
            conditon_list = []
            for key in list(conditions.keys()):
                if self.params.get(key, None):
                    conditon_list.append(self.params.get(key) == conditions.get(key))
            conditions = conditon_list
        else:
            conditions = []

        query = self.session.query(Proxy.ip, Proxy.port)
        if len(conditions) > 0 and count:
            for condition in conditions:
                query = query.filter(condition)
            return query.order_by(Proxy.speed).limit(count).all()
        elif count:
            return query.order_by(Proxy.speed).limit(count).all()
        elif len(conditions) > 0:
            for condition in conditions:
                query = query.filter(condition)
            return query.order_by(Proxy.speed).all()
        else:
            return query.order_by(Proxy.speed).all()

    def close(self):
        pass
