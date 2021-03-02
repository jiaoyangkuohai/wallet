import os

from PyQt5.QtWidgets import QWidget, QDialogButtonBox, QDialog, QFileDialog
from PyQt5.QtCore import QDate, Qt

from uis.setting import Ui_Dialog
from database import DBField
from utils import settings, Configs


class SettingWindow(QDialog, Ui_Dialog):
    def __init__(self, update_signal):
        super().__init__()
        self.setupUi(self)
        self.update_singal = update_signal
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("取消")
        self.buttonBox.button(QDialogButtonBox.Ok).setText("确定")

        self.comboBox.addItems(DBField.db_type)

        self._init_date()

        self.pushButton.clicked.connect(self.about_path)
        self.use_settings_line_edit()

        self.pushButton_2.clicked.connect(self._init_date)

    def accept(self) -> None:
        settings.setValue(Configs.db_path, self.lineEdit.text())
        settings.setValue(Configs.start_time, self.dateEdit.text())
        settings.setValue(Configs.end_time, self.dateEdit_2.text())
        self.update_singal.emit()
        super().accept()

    def reject(self) -> None:
        # print("reject")
        self.use_settings_line_edit()
        self.use_setting_date_value()
        super().reject()

    def _init_date(self):
        # print("__int date")
        # 日期设置
        current = QDate.currentDate()
        self.dateEdit.setDate(QDate(current.year(), current.month(), 1))
        self.dateEdit.setDisplayFormat("yyyy-MM-dd")

        self.dateEdit_2.setDate(current)
        self.dateEdit_2.setDisplayFormat("yyyy-MM-dd")

        if settings.value(Configs.start_time) is None:
            settings.setValue(Configs.start_time, self.dateEdit.text())
        if settings.value(Configs.end_time) is None:
            settings.setValue(Configs.end_time, self.dateEdit_2.text())

    def use_settings_line_edit(self):
        self.lineEdit.setText(settings.value(Configs.db_path))

    def use_setting_date_value(self):
        start_time = settings.value(Configs.start_time)
        self.dateEdit.setDate(QDate.fromString(start_time, "yyyy-MM-dd"))
        end_time = settings.value(Configs.end_time)
        self.dateEdit_2.setDate(QDate.fromString(end_time, "yyyy-MM-dd"))

    def about_path(self):
        dir = QFileDialog.getExistingDirectory(self, "选取文件", "./")
        if self.comboBox.currentText() == DBField.db_type[0]:
            db_path = os.path.abspath(os.path.join(dir, Configs.default_db_name))
            self.lineEdit.setText(db_path)
            # print(db_path)
