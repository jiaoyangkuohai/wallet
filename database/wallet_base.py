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


class DBOperation(object):
    @classmethod
    def get_instance(cls, *args, **kwargs):
        ops = DBOps["sqlite3"]
        return ops. get_instance(*args, **kwargs)

    # 增
    def insert_one(self, *args, **kwargs):
        raise NotImplemented

    # 删
    def delete_one(self, *args, **kwargs):
        raise NotImplemented

    # 查
    def search_more(self, *args, **kwargs):
        raise NotImplemented

    def search_all(self):
        raise NotImplemented

    # 按照时间段查询
    def search_range(self, *args, **kwargs):
        raise NotImplemented

    # 改
    def update_one(self, *args, **kwargs):
        raise NotImplemented

    def commit(self, *args, **kwargs):
        raise NotImplemented

    # 提交并关闭数据库
    def close_database(self, *args, **kwargs):
        raise NotImplemented
