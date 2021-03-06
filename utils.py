import os
import re

from PyQt5.QtCore import Qt, QModelIndex, QSettings, QTextCodec


# class Setting:
#     def __init__(self):
#         self.db_path = ""

class DBField:
    id = "id"
    dateInput = "dateInput"
    firstClassifier = "firstClassifier"
    secondClassifier = "secondClassifier"
    inOut = "inOut"
    inOutClassifier = "inOutClassifier"
    inOutSelect = ["支出", "收入"]

    db_type = ["sqlite3", "mysql"]

class Configs:
    db_path = "db_path"
    start_time = "start_time"
    end_time = "end_time"
    default_db_name = "wallet_data.db"
    first_classifier = "first_classifier"
    second_classifier = "second_classifier"
    db_used = "db_used"

    mysql_host = "host"
    mysql_port = "port"
    mysql_user = "user_name"
    mysql_password = "password"
    mysql_database = "database"
    mysql_table = "table"


def _get_settings(config_dir=None):
    """
    配置文件
    """
    if config_dir is None:
        config_dir = os.path.join(os.path.abspath(os.path.curdir), "wallet_config")

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    config_file = os.path.join(config_dir, "config.ini")

    settings_obj = QSettings(config_file, QSettings.IniFormat)
    settings_obj.setIniCodec(QTextCodec.codecForName("utf-8"))

    if settings_obj.value(Configs.db_used) is None:
        settings_obj.setValue(Configs.db_used, DBField.db_type[0])

    if settings_obj.value(Configs.db_path) is None:
        settings_obj.setValue(Configs.db_path, os.path.abspath(os.path.join("./", Configs.default_db_name)))

    return settings_obj


settings = _get_settings()


def check_price(price):
    """检查价格的输入是否符合规则"""
    out = re.fullmatch(r"^[-]?[0-9]+\.?[0-9]*", price)
    if out is None:
        return False
    return True


def process_date(date="2021-02-27"):
    return date
    # if date is None:
    #     return date
    # y, m, d = date.split("-")
    # return "-".join([y, str(int(m)), str(int(d))])
