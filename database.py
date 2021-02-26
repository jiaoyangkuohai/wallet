import os
import sqlite3

import pandas as pd


class DBField:
    id = "id"
    firstClassifier = "firstClassifier"
    secondClassifier = "secondClassifier"
    inOut = "inOut"
    inOutClassifier = "inOutClassifier"
    inOutSelect = ["支出", "收入"]


class DBOperation:
    """
    数据库的一系列操
    增删查改
    """
    def __init__(self):
        self.conn, self.cursor = self.get_conn()

    @classmethod
    def get_instance(cls):
        return cls()

    # 获取游标
    def get_conn(self):
        database_path = "./data/data.db"
        create_table = True if not os.path.exists(database_path) else False
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        if create_table:
            cursor.execute("create table wallet(id INTEGER PRIMARY KEY AUTOINCREMENT, date text, inOutClassifier text, firstClassifier text, secondClassifier text, inOut real)")
        return conn, cursor

    # 增
    def insert_one(self, date='2020-10-05', inOutClassifier="支出", firstClass='衣', secondClass='唯品会', price=300):
        self.cursor.execute("insert into wallet values(null,?,?, ?,?,?)", (date, inOutClassifier, firstClass, secondClass, price))


    # 删
    def delete_one(self, id=1):
        self.cursor.execute("delete from wallet where id=?", (id,))


    # 查
    def search_more(self, date='2020-10-04'):
        sql = "select * from wallet where date=?"
        df = pd.read_sql(sql, self.conn, params=(date,))
        print(df)
        return df

    def search_all(self):
        sql = "select * from wallet"
        df = pd.read_sql(sql, self.conn)
        print(df)
        return df

    # 改
    def update_one(self, id=2, date='2020-10-04',inOutClassifier="支出", firstClass='衣', secondClass='唯品会', price=4000):
        self.cursor.execute("update wallet set date=?, inOutClassifier=?, firstClassifier=?, secondClassifier=?, inOut=? where id=?", (date, inOutClassifier, firstClass, secondClass, price, id))

    def commit(self):
        self.conn.commit()

    # 提交并关闭数据库
    def close_database(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

def save_data():
    sqlite3_db = DBOperation()
    sqlite3_db.insert_one()
    sqlite3_db.search_more()
    sqlite3_db.delete_one()
    sqlite3_db.search_more()
    sqlite3_db.update_one()
    df = sqlite3_db.search_more()
    df = df.set_index("id")
    sqlite3_db.search_all()
    df.to_csv("./data/out.csv")
    sqlite3_db.close_database()


def about_list():
    sqlite3_db = DBOperation()
    df = sqlite3_db.search_all()
    print(df)
    sqlite3_db.close_database()
    a = df.firstClassifier.tolist()
    b = df.inOut.tolist()
    print(a)
    print(b)


if __name__ == '__main__':
    # save_data()
    about_list()
