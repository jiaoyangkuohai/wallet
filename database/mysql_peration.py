# -*- coding:utf-8 -*-
"""
@author    : shihongliang
@time      : 2021-03-13 8:05
@filename  : mysql_peration.py
"""

import pymysql
import pandas as pd
import numpy as np

from database.wallet_base import DBOperation
from database import register_model


# @register_model("mysql")
class MySQLDBOperation(DBOperation):
    """
    MySQL数据库的一系列操作
    """
    def __init__(self, *args, **kwargs):
        self.conn, self.cursor = self.get_conn(**kwargs)

    def get_conn(self, host, user, password, database):
        conn = pymysql.connect(host=host,
                               user=user,
                               password=password,
                               database=database)
        cursor = conn.cursor()
        return conn, cursor

    @classmethod
    def get_instance(cls, *args, **kwargs):

        return cls(*args, **kwargs)

    def insert_one(self, dateInput='2020-12-05', inOutClassifier="支出", firstClass='衣', secondClass='唯品会', price=300):
        self.cursor.execute("insert into wallet values(null,'{}','{}', '{}','{}',{})".format(dateInput, inOutClassifier, firstClass, secondClass, price))

    def delete_one(self, id=1):
        self.cursor.execute("delete from wallet where id={}".format(id))

    def search_more(self, dateInput='2020-10-04'):
        sql = "select * from wallet where dateInput='{}'".format(dateInput)
        df = pd.read_sql(sql, self.conn)
        return df

    def search_all(self):
        sql = "select * from wallet"
        df = pd.read_sql(sql, self.conn)
        return df

    def search_range(self, start, end):
        sql = "select * from wallet where dateInput>='{}' and dateInput<='{}'".format(start, end)
        df = pd.read_sql(sql, self.conn)
        return df

    def update_one(self, id=2,
                   dateInput='2020-10-04',
                   inOutClassifier="支出",
                   firstClass='衣',
                   secondClass='唯品会',
                   price=4000):
        self.cursor.execute(
            "update wallet set dateInput='{}', inOutClassifier='{}', firstClassifier='{}', secondClassifier='{}', `inOut`={} where id={}".format(dateInput, inOutClassifier, firstClass, secondClass, price, id))

    def commit(self):
        return self.conn.commit()

    def close_database(self, *args, **kwargs):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

