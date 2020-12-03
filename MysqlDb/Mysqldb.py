import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from matplotlib import font_manager
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Date, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from Others.logging_file import logger

my_font = font_manager.FontProperties(fname="C:\Windows\Fonts\PingFang.ttc")

Base = declarative_base()  # 创建基类
engine = create_engine("mysql+pymysql://root:981225@localhost/mysqldb?charset=utf8", encoding="utf-8")
# print("创建数据库引擎")
DBSession = sessionmaker(bind=engine)
session = DBSession()



# class Users(Base):
#     __tablename__ = 'Users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(32))
#     extra = Column(String(16))
#
#     __table_args__ = (
#     UniqueConstraint('id', 'name', name='uix_id_name'),
#         Index('ix_id_name', 'name', 'extra'),
#     )



# 供应商
class Producer(Base):
    __tablename__ = 'Producer'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    produce_total = Column(Integer, nullable=False)

    def __repr__(self):
        return "Producer"



# 销售商
class Cosumer(Base):
    __tablename__ = 'Cosumer'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    Cosumer_total = Column(Integer, nullable=False)

    def __repr__(self):
        return "Cosumer"

#
class Cost(Base):
    __tablename__ = 'Cost'
    id = Column(Integer, primary_key=True)
    # a_id = Column(Integer, ForeignKey("Producer.id"))
    # b_id = Column(Integer, ForeignKey("Cosumer.id"))
    cost = Column(String(200), default=0)


class Profit(Base):
    __tablename__ = 'Profit'

    id = Column(Integer, primary_key=True)

    # a_id = Column(Integer, ForeignKey("Producer.id"))
    # b_id = Column(Integer, ForeignKey("Cosumer.id"))

    profit = Column(String(200), default=0)


# 初始化数据库
def initdb():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


# 插入数据
def insert(new_data):
    Base = declarative_base()
    # 修改用户名、密码、数据库的名字
    engine = create_engine("mysql+pymysql://root:981225@localhost/mysqldb?charset=utf8", encoding="utf-8")
    print("创建数据库引擎")
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    session.add(new_data)
    print("添加数据到session")

    session.commit()
    print("提交数据到数据库")

    session.close()
    print("关闭数据库连接")

# 更改数据
def update(update_data, update_class, filters):
    '''
    更新单个数据
    :param update_data: dict {name: 'aa', Cosumer_total: 11}
    :param update_class: Cosumer
    :param filters: list [1]
    :return:
    '''
    engine = create_engine("mysql+pymysql://root:981225@localhost/mysqldb?charset=utf8", encoding="utf-8")
    # print("创建数据库引擎")

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    update_classes = session.query(update_class).filter_by(id=filters).first()
    for key, value in update_data.items():
        # key1 = eval(key)
        setattr(update_classes, key, value)
        # print("finished")
    session.commit()
    session.close()

# 查找数据
def query_data(query_class, filters):
    engine = create_engine("mysql+pymysql://root:981225@localhost/mysqldb?charset=utf8", encoding="utf-8")
    # print("创建数据库引擎")

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    query_classes = session.query(query_class).filter_by(id=filters).all()

    return query_classes


def add_data_producer(data):
    assert type(data) == list
    data_len = len(data)
    for i in range(data_len):
        # print(session.query(Producer).filter_by(id=i+1).all())
        if session.query(Producer).filter_by(id=i+1).all():
            update({'produce_total': data[i]}, Producer, i+1)
        else:
            new_producer = Producer(id=i+1, name='A_{}'.format(i+1), produce_total=data[i])
            insert(new_producer)

    logger.info("insert data into producerdb: {}".format(data))





def add_data_cosumer(data):
    assert type(data) == list
    data_len = len(data)
    for i in range(data_len):
        # print(session.query(Producer).filter_by(id=i+1).all())
        if session.query(Cosumer).filter_by(id=i+1).all():
            update({'Cosumer_total': data[i]}, Cosumer, i+1)
        else:
            new_cosumer = Cosumer(id=i+1, name='B_{}'.format(i+1), Cosumer_total=data[i])
            insert(new_cosumer)

    logger.info("insert data into cosumerdb: {}".format(data))


# Session = sessionmaker(bind=engine)
# session = Session()


# def computer_express():
#
#
#
# def computer_profit():
#     pass
#
#
# def compute_total_profit():
#     pass

if __name__ == '__main__':
    # initdb()
    data = [2, 3, 3, 4, 5]
    add_data_cosumer(data)

