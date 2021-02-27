import os
import sqlite3

import pandas as pd
from database import register_model
from database import DBOps

class DBField:
    id = "id"
    firstClassifier = "firstClassifier"
    secondClassifier = "secondClassifier"
    inOut = "inOut"
    inOutClassifier = "inOutClassifier"
    inOutSelect = ["支出", "收入"]

    db_type = ["sqlite3", "mysql"]


class DBOperation:
    @classmethod
    def get_instance(cls):
        ops = DBOps["sqlite3"]
        return ops.get_instance()

    # 增
    def insert_one(self, date='2020-10-05', inOutClassifier="支出", firstClass='衣', secondClass='唯品会', price=300):
        NotImplemented

    # 删
    def delete_one(self, id=1):
        NotImplemented

    # 查
    def search_more(self, date='2020-10-04'):
        NotImplemented

    def search_all(self):
        NotImplemented

    # 改
    def update_one(self, id=2, date='2020-10-04',inOutClassifier="支出", firstClass='衣', secondClass='唯品会', price=4000):
        NotImplemented

    def commit(self):
        NotImplemented

    # 提交并关闭数据库
    def close_database(self):
        NotImplemented
