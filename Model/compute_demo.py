import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy import optimize as op
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from MysqlDb.Mysqldb import Producer, Cosumer, Cost, Profit
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from Others.logging_file import logger, init_logger
from pymprog import *

# 初始化logging
# init_logger('logging.txt')

engine = create_engine("mysql+pymysql://root:981225@localhost/mysqldb?charset=utf8", encoding="utf-8")
DBSession = sessionmaker(bind=engine)
session = DBSession()


def solve_problem(c, min_or_max=True):
    n_producer = len(session.query(Producer).all())
    n_cosumer = len(session.query(Cosumer).all())
    # 建立变量
    a = []
    b = []

    for i in range(n_producer):
        a.append("A_{x}".format(x=i+1))  # 产地

    for j in range(n_cosumer):
        b.append("B_{x}".format(x=j+1))  # 销地
    print(a)
    print(b)
    # c = []

    # 取数据

    # cost = session.query(price_object).all()
    # for cos in cost:
    #     c.append(eval(cos.cost))

    # a = ('A1', 'A2', 'A3')        # 产地
    # b = ('B1', 'B2', 'B3', 'B4')  # 销地

    price = dict()
    for i in a:
        for j in b:
            if j == len(b) - 1:
                price[i, j] = 0
            else:
                price[i, j] = c[a.index(i)][b.index(j)]


    # 产地
    d = []
    produce = dict()
    producer = session.query(Producer).all()
    for pro in producer:
        d.append(pro.produce_total)
    # d = [60, 55, 51]
    for i in a:
        produce[i] = d[a.index(i)]

    # 销量
    e = []
    sale = dict()
    cosumer = session.query(Cosumer).all()
    for cos in cosumer:
        e.append(cos.Cosumer_total)
    # e = [35, 37, 72, 22]
    for i in b:
        sale[i] = e[b.index(i)]
    #
    # print("(产地,销地):运价\n", price)
    # print("\n产地:产量\n", produce)
    # print("\n销地:销量\n", sale)

    # 模型及求解
    begin("transport")
    x = var('x', price.keys())
    if min_or_max:
        minimize(sum(price[i, j]*x[i, j] for (i, j) in price.keys()), 'Cost')  # 总运费最少
    else:
        maximize(sum(price[i, j]*x[i, j] for (i, j) in price.keys()), 'Cost')
    for i in produce.keys():                                               # 产地产量约束
        sum(x[i, j] for j in sale.keys()) == produce[i]
    for j in sale.keys():                                                  # 销地销量约束
        sum(x[i ,j] for i in produce.keys()) == sale[j]

    solve()
    result = vobj()
    # report()
    end()
    return result, x, price

def computer_express(c):
    return solve_problem(c)


def computer_profit(p):
    return solve_problem(p, False)



def compute_total_profit(tp):
    return solve_problem(tp, False)
if __name__ == '__main__':

    c = [[6, 2, 6, 0],
         [4, 9, 5, 0],
         [5, 2, 1, 0],
         ]
    print(computer_express(c))