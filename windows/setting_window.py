import os

from PyQt5.QtWidgets import QWidget, QDialogButtonBox, QDialog, QFileDialog
from PyQt5.QtCore import QDate

from uis.setting import Ui_Dialog
from database import DBField


class SettingWindow(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("取消")
        self.buttonBox.button(QDialogButtonBox.Ok).setText("确定")

        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.close)
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.add_setting)

        self.comboBox.addItems(DBField.db_type)

        # 日期设置
        current = QDate.currentDate()
        self.dateEdit.setDate(QDate(current.year(), current.month(), 1))
        self.dateEdit.setDisplayFormat("yyyy-MM-dd")

        self.dateEdit_2.setDate(current)
        self.dateEdit_2.setDisplayFormat("yyyy-MM-dd")

        self.pushButton.clicked.connect(self.about_path)

    def add_setting(self):
        print("clicked ok")
        self.close()

    def about_path(self):
        dir = QFileDialog.getExistingDirectory(self, "选取文件", "./")
        if self.comboBox.currentText() == DBField.db_type[0]:
            db_path = os.path.abspath(os.path.join(dir, "wallet_data.db"))
            self.lineEdit.setText(db_path)
            print(db_path)
