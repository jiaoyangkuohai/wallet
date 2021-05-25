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
from database import register_model, SqliteDBOperation
from utils import DBField, settings, Configs


@register_model(DBField.db_type[1])
class MySQLDBOperation(DBOperation):
    """
    MySQL数据库的一系列操作
    """
    def __init__(self, *args, **kwargs):
        self.conn, self.cursor = self.get_conn(**kwargs)

    def get_conn(self, *args, **kwargs):
        conn = pymysql.connect(host=settings.value(Configs.mysql_host),
                               user=settings.value(Configs.mysql_user),
                               password=settings.value(Configs.mysql_password),
                               database=settings.value(Configs.mysql_database),
                               port=int(settings.value(Configs.mysql_port)))
        cursor = conn.cursor()
        conn.ping()
        return conn, cursor

    @classmethod
    def get_instance(cls, *args, **kwargs):
        try:
            return cls(*args, **kwargs)
        except Exception as e:
            settings.setValue(Configs.db_used, DBField.db_type[0])
            return SqliteDBOperation.get_instance()

    def insert_one(self, dateInput='2020-12-05', inOutClassifier="支出", firstClass='衣', secondClass='唯品会', price=300):
        try:
            table_name = settings.value(Configs.mysql_table)
            self.cursor.execute("insert into {} values(null,'{}','{}', '{}','{}',{})".format(table_name, dateInput, inOutClassifier, firstClass, secondClass, price))
        except Exception as e:
            pass

    def delete_one(self, id=1):
        try:
            table_name = settings.value(Configs.mysql_table)
            self.cursor.execute("delete from {} where id={}".format(table_name, id))
        except Exception as e:
            pass

    def search_more(self, dateInput='2020-10-04'):
        try:
            table_name = settings.value(Configs.mysql_table)
            sql = "select * from {} where dateInput='{}'".format(table_name, dateInput)
            df = pd.read_sql(sql, self.conn)
            return df
        except Exception as e:
            return self._panda_df()

    def search_all(self):
        try:
            table_name = settings.value(Configs.mysql_table)
            sql = "select * from {}".format(table_name)
            df = pd.read_sql(sql, self.conn)
            return df
        except Exception as e:
            return self._panda_df()

    def search_range(self, start, end):
        try:
            table_name = settings.value(Configs.mysql_table)
            sql = "select * from {} where dateInput>='{}' and dateInput<='{}' order by dateInput".format(table_name, start, end)
            df = pd.read_sql(sql, self.conn)
            return df
        except Exception as e:
            return self._panda_df()

    def update_one(self, id=2,
                   dateInput='2020-10-04',
                   inOutClassifier="支出",
                   firstClass='衣',
                   secondClass='唯品会',
                   price=4000):
        try:
            table_name = settings.value(Configs.mysql_table)
            self.cursor.execute(
                "update {} set dateInput='{}', inOutClassifier='{}', firstClassifier='{}', secondClassifier='{}', `inOut`={} where id={}".format(table_name, dateInput, inOutClassifier, firstClass, secondClass, price, id))
        except Exception as e:
            pass

    def _panda_df(self):
        return pd.DataFrame(columns=[DBField.id, DBField.dateInput, DBField.inOutClassifier,
                                     DBField.firstClassifier, DBField.secondClassifier, DBField.inOut])

    def commit(self):
        return self.conn.commit()

    def close_database(self, *args, **kwargs):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

