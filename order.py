# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 20:48:50 2018

@author: Prodipta
"""

from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

table_name = 'orders'
logger = logging.getLogger(__name__)
    
Base = declarative_base()
class Order(Base):
    __tablename__ = table_name
    
    order_id = Column(String(250), unique=True, primary_key=True)
    placed_by = Column(String(250))
    status = Column(String(250), nullable=False)
    status_message = Column(String(1024))
    tradingsymbol = Column(String(250), nullable=False)
    exchange = Column(String(250))
    order_type = Column(String(250))
    transaction_type = Column(String(250), nullable=False)
    validity = Column(String(250))
    product = Column(String(250))
    average_price = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    filled_quantity = Column(Integer, nullable=False)
    unfilled_quantity = Column(Integer, nullable=False)
    trigger_price = Column(Float)
    user_id = Column(String(250))
    order_timestamp = Column(String(250), nullable=False)
    exchange_timestamp = Column(String(250))
    
    def __init__(self,order_dict):
        self.from_dict(order_dict)
        
    def from_dict(self, order_dict):
        self.order_id = order_dict.get("order_id", None)
        self.placed_by = order_dict.get("placed_by", None)
        self.status = order_dict.get("status", None)
        self.status_message = order_dict.get("status_message", "")
        self.tradingsymbol = order_dict.get("tradingsymbol", None)
        self.exchange = order_dict.get("exchange", None)
        self.order_type = order_dict.get("order_type", None)
        self.transaction_type = order_dict.get("transaction_type", None)
        self.validity = order_dict.get("validity", None)
        self.product = order_dict.get("product", None)
        self.average_price = order_dict.get("average_price", None)
        self.price = order_dict.get("price", None)
        self.quantity = order_dict.get("quantity", None)
        self.filled_quantity = order_dict.get("filled_quantity", None)
        self.unfilled_quantity = order_dict.get("unfilled_quantity", None)
        self.trigger_price = order_dict.get("trigger_price", None)
        self.user_id = order_dict.get("user_id", None)
        self.order_timestamp = order_dict.get("order_timestamp", None)
        self.exchange_timestamp = order_dict.get("exchange_timestamp", None)
        
    def to_dict(self):
        return vars(self)
    
    def __repr__(self):
        return str(self.to_dict())
    
    def update(self, order_dict):
        if self.order_id != order_dict.get("order_id", None):
            raise ValueError('order ID does not match.')
        self.from_dict(order_dict)
        

class OrderWriter(object):
    def __init__(self, path):
        self.path = path
        self.engine = create_engine('sqlite:///' + self.path)
        self.metadata = Base.metadata
        self.Session = sessionmaker(bind=self.engine)
        with self.engine.begin() as conn:
            self._init_db(conn)
    
    def _init_db(self,conn):
        self.metadata.create_all(conn, checkfirst=True)
        
    def upsert(self,order):
        if isinstance(order,dict):
            order = Order(order)
            
        if not isinstance(order, Order):
            raise TypeError('input must be of class Order')
            
        session = self.Session()
        self.insert_or_update(session,order)
        session.commit()
        session.flush()
            
    def insert_or_update(self, session, order):
        x = session.query(Order).filter(Order.order_id == order.order_id).first()
        if x != None:
            logger.info('updating order id'+order.order_id+'...\n')
            x.update(order.to_dict())
        else:
            logger.info('inserting order id'+order.order_id+'...\n')
            session.add(order)

            
            
