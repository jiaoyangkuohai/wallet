import os
import sqlite3

import pandas as pd

from database.wallet_base import DBOperation
from database import register_model

from utils import settings, Configs, process_date, DBField


@register_model(DBField.db_type[0])
class SqliteDBOperation(DBOperation):
    """
    数据库的一系列操
    增删查改
    """
    def __init__(self, db_path):
        self.conn, self.cursor = self.get_conn(db_path)

    @classmethod
    def get_instance(cls, *args, **kwargs) -> DBOperation:
        return cls(settings.value(Configs.db_path))

    # 获取游标
    # todo 不能每次都连接
    def get_conn(self, database_path):
        create_table = True if not os.path.exists(database_path) else False
        # print("db_path: {}".format(database_path))
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        if create_table:
            cursor.execute("create table wallet(id INTEGER PRIMARY KEY AUTOINCREMENT, dateInput date, inOutClassifier text, firstClassifier text, secondClassifier text, inOut real)")
        return conn, cursor

    # 增
    def insert_one(self, dateInput='2020-10-05', inOutClassifier="支出", firstClass='衣', secondClass='唯品会', price=300):
        self.cursor.execute("insert into wallet values(null,?,?, ?,?,?)", (dateInput, inOutClassifier, firstClass, secondClass, price))


    # 删
    def delete_one(self, id=1):
        self.cursor.execute("delete from wallet where id=?", (id,))

    # 查
    def search_more(self, dateInput='2020-10-04'):
        sql = "select * from wallet where dateInput=?"
        df = pd.read_sql(sql, self.conn, params=(process_date(dateInput),))
        # print(df)
        return df

    def search_all(self):
        sql = "select * from wallet"
        df = pd.read_sql(sql, self.conn)
        return df

    # 按照时间段查询
    def search_range(self, start, end):
        sql = "select * from wallet where dateInput>=? and dateInput<=? order by dateInput"
        df = pd.read_sql(sql, self.conn, params=(process_date(start), process_date(end)))
        # print("search range: {} and {}".format(start, end))
        # print(df)
        return df

    # 改
    def update_one(self, id=2, dateInput='2020-10-04',inOutClassifier="支出", firstClass='衣', secondClass='唯品会', price=4000):
        self.cursor.execute("update wallet set dateInput=?, inOutClassifier=?, firstClassifier=?, secondClassifier=?, inOut=? where id=?", (dateInput, inOutClassifier, firstClass, secondClass, price, id))

    def commit(self):
        self.conn.commit()

    # 提交并关闭数据库
    def close_database(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


# def save_data():
#     sqlite3_db = SqliteDBOperation()
#     sqlite3_db.insert_one()
#     sqlite3_db.search_more()
#     sqlite3_db.delete_one()
#     sqlite3_db.search_more()
#     sqlite3_db.update_one()
#     df = sqlite3_db.search_more()
#     df = df.set_index("id")
#     sqlite3_db.search_all()
#     df.to_csv("./data/out.csv")
#     sqlite3_db.close_database()


def about_list():
    import datetime
    sqlite3_db = SqliteDBOperation("F:\\wallet\\mytest\\wallet_data.db")
    df = sqlite3_db.search_all()
    print(df)
    t = datetime.datetime.strptime('2021-02-01', '%Y-%m-%d')
    dt = datetime.date(t.year, t.month, t.day)

    # t2 = datetime.datetime.strptime('2021-02-27', '%Y-%m-%d')
    # dt2 = datetime.date(t2.year, t2.month, t2.day)

    df2 = sqlite3_db.search_range('2021-02-01', '2021-02-27')
    print(df2)
    df3 = sqlite3_db.search_more("2021-2-27")
    print(df3)

    print("...")
    out = sqlite3_db.cursor.execute("select * from wallet where dateInput='2021-2-27'")
    [print(i) for i in out]

    # sqlite3_db.close_database()
    # a = df.firstClassifier.tolist()
    # b = df.inOut.tolist()
    # print(a)
    # print(b)


if __name__ == '__main__':
    about_list()