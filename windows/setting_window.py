import sys
import os

from PyQt5.QtWidgets import QWidget, QTableWidget, QFileDialog, QDialogButtonBox, QDialog, QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.Qt import QUrl, QFileInfo, QDate

from uis.setting import Ui_Dialog
from uis.db_sqlite3 import Ui_Form as SQLiteForm
from uis.db_mysql import Ui_Form as MySQLForm

from utils import settings, Configs, DBField


class SQLiteWidget(QWidget, SQLiteForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class MySQLWidget(QWidget, MySQLForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class SettingWindow(QDialog, Ui_Dialog):
    def __init__(self, update_signal):
        super().__init__()
        self.setupUi(self)

        self._init_radio_frame()
        self.radioButton.toggled.connect(self.use_different_windows)
        self.radioButton_2.toggled.connect(self.use_different_windows)


        self.update_singal = update_signal
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("取消")
        self.buttonBox.button(QDialogButtonBox.Ok).setText("确定")

        self._init_date()

        self.page.pushButton.clicked.connect(self.about_path)
        self.use_settings_line_edit()

        self.pushButton_2.clicked.connect(self._init_date)

    def accept(self) -> None:
        settings.setValue(Configs.db_path, self.page.lineEdit.text())
        self.set_mysql_info()
        settings.setValue(Configs.start_time, self.dateEdit.text())
        settings.setValue(Configs.end_time, self.dateEdit_2.text())
        self._set_radio()
        self.update_singal.emit()
        super().accept()

    def reject(self) -> None:
        # print("reject")
        self.use_settings_line_edit()
        self.use_setting_date_value()
        self.get_mysql_info()
        self._rollback_radio()
        super().reject()

    def set_mysql_info(self):
        """
        将MySQL数据库信息保存到配置文件
        """
        settings.setValue(Configs.mysql_host, self.page_2.lineEdit.text())
        settings.setValue(Configs.mysql_port, self.page_2.lineEdit_2.text())
        settings.setValue(Configs.mysql_user, self.page_2.lineEdit_3.text())
        settings.setValue(Configs.mysql_password, self.page_2.lineEdit_4.text())
        settings.setValue(Configs.mysql_database, self.page_2.lineEdit_5.text())
        settings.setValue(Configs.mysql_table, self.page_2.lineEdit_6.text())

    def get_mysql_info(self):
        """
        将MySQL数据库信息恢复的原信息
        """
        self.page_2.lineEdit.setText(settings.value(Configs.mysql_host))
        self.page_2.lineEdit_2.setText(settings.value(Configs.mysql_port))
        self.page_2.lineEdit_3.setText(settings.value(Configs.mysql_user))
        self.page_2.lineEdit_4.setText(settings.value(Configs.mysql_password))
        self.page_2.lineEdit_5.setText(settings.value(Configs.mysql_database))
        self.page_2.lineEdit_6.setText(settings.value(Configs.mysql_table))

    def use_different_windows(self):
        # 使用不同的窗口
        if self.radioButton.isChecked():
            self.page.lineEdit.setText(settings.value(Configs.db_path))
            self.stackedWidget.setCurrentIndex(0)
        elif self.radioButton_2.isChecked():
            self.stackedWidget.setCurrentIndex(1)

    def _init_radio_frame(self):
        """
        初始化界面显示哪个数据库信息
        """
        if settings.value(Configs.db_used) == DBField.db_type[0]:
            self.radioButton.setChecked(True)
            self.stackedWidget.setCurrentIndex(0)
        elif settings.value(Configs.db_used) == DBField.db_type[1]:
            self.radioButton_2.setChecked(True)
            self.stackedWidget.setCurrentIndex(1)

    def _init_date(self):
        # 日期设置
        current = QDate.currentDate()
        self.dateEdit.setDate(QDate(current.year(), current.month(), 1))
        self.dateEdit.setDisplayFormat("yyyy-MM-dd")

        self.dateEdit_2.setDate(current)
        self.dateEdit_2.setDisplayFormat("yyyy-MM-dd")

        settings.setValue(Configs.start_time, self.dateEdit.text())
        settings.setValue(Configs.end_time, self.dateEdit_2.text())

    def _rollback_radio(self):
        if settings.value(Configs.db_used) == DBField.db_type[0]:
            self.radioButton.setChecked(True)
        else:
            self.radioButton_2.setChecked(True)

    def _set_radio(self):
        if self.radioButton.isChecked():
            settings.setValue(Configs.db_used, DBField.db_type[0])
        elif self.radioButton_2.isChecked():
            settings.setValue(Configs.db_used, DBField.db_type[1])

    def use_settings_line_edit(self):
        """
        设置数据库的相关信息
        """
        self.page.lineEdit.setText(settings.value(Configs.db_path))
        self.get_mysql_info()

    def use_setting_date_value(self):
        """
        将日期恢复到原值
        """
        start_time = settings.value(Configs.start_time)
        self.dateEdit.setDate(QDate.fromString(start_time, "yyyy-MM-dd"))
        end_time = settings.value(Configs.end_time)
        self.dateEdit_2.setDate(QDate.fromString(end_time, "yyyy-MM-dd"))

    def about_path(self):
        dir = QFileDialog.getExistingDirectory(self, "选取文件", "./")
        if self.radioButton.isChecked():
            db_path = os.path.abspath(os.path.join(dir, Configs.default_db_name))
            self.page.lineEdit.setText(db_path)

    def exec(self) -> int:
        self._rollback_radio()
        return super().exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = 2
    demo = SettingWindow(a)
    demo.show()
    sys.exit(app.exec_())

