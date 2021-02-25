from PyQt5.QtWidgets import QWidget, QDialogButtonBox, QDialog

from uis.setting import Ui_Dialog


class SettingWindow(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("取消")
        self.buttonBox.button(QDialogButtonBox.Ok).setText("确定")

        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.close)
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.add_setting)

    def add_setting(self):
        print("clicked ok")
        self.close()
