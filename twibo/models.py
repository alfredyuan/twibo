from sqlalchemy import (
    Column,
    Table,
    ForeignKey,
    Integer,
    Text,
    String,
    DateTime,
    Boolean
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    relationship,
    backref,
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

from datetime import datetime

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    value = Column(Integer)

    def __init__(self, name, value):
        self.name = name
        self.value = value

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    tw_name = Column(String(255), unique=True)
    wi_account_name = Column(String(255), unique=True)
    wi_account_pwd = Column(String(255))
    register_time = Column(DateTime)
    auto_sync = Column(Boolean, default=False)
    profile_pic = Column(String(500), nullable=True)

    def __init__(self, tw_name):
        self.tw_name = tw_name
        self.register_time = datetime.now()
        # self.wi_account_name = wi_account_name
        # self.wi_account_pwd = wi_account_pwd

class Tweet(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)
    text = Column(String(255), nullable=False)
    twitter_id = Column(String(50), nullable=False)
    original_time = Column(DateTime, nullable=False)

    weibo = relationship("Weibo", uselist=False, backref="Tweet")
    
    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship('Customer', backref="tweets")

    def __init__(self, tweet, customer_id):
        self.text = tweet.text.encode('utf-8')
        self.twitter_id = tweet.id
        self.original_time = datetime.strptime(tweet.created_at,'%a %b %d %H:%M:%S +0000 %Y')
        self.customer_id = customer_id

class Weibo(Base):
    __tablename__ = 'weibos'
    id = Column(Integer, primary_key=True)
    text = Column(String(255), nullable=False)
    weibo_id = Column(String(50), nullable=False)
    thumbnail_pic = Column(String(500), nullable=True)
    bmiddle_pic = Column(String(500), nullable=True)
    original_pic = Column(String(500), nullable=True)
    syndicate_time = Column(DateTime, nullable=True)
    tweet_id = Column(Integer, ForeignKey('tweets.id'))

    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship('Customer', backref="weibos")

    def __init__(self, weibo, tweet_id, customer_id):
        self.text = weibo.text.encode('utf-8')
        self.weibo_id = weibo.id
        #self.thumbnail_pic = weibo.thumbnail_pic
        #self.bmiddle_pic = weibo.bmiddle_pic
        #self.original_pic = weibo.original_pic
        self.syndicate_time = datetime.now()
        self.tweet_id = tweet_id
        self.customer_id = customer_id

class TwiboEngineLog(Base):
    __tablename__ = 'twibo_engine_logs'
    id = Column(Integer, primary_key=True)
    log_time = Column(DateTime, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=True)
    top_log = Column(String(50), nullable=False)
    sec_log = Column(String(50), nullable=True)
    detail_log = Column(Text(), nullable=True)

    customer = relationship('Customer', backref='logs')

    def __init__(self, top_log, customer_id=None, sec_log=None, detail_log=None):
        self.log_time = datetime.now()
        self.top_log = top_log
        self.sec_log = sec_log
        self.detail_log = detail_log
        self.customer_id = customer_id
