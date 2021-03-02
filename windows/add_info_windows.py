import re
from PyQt5.QtWidgets import QDialogButtonBox, QDialog

from uis.add_info import Ui_Dialog
from database import DBOperation, DBField
from utils import settings, Configs, check_price


class AddInfoWindow(QDialog, Ui_Dialog):
    def __init__(self, update_signal):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("取消")
        self.buttonBox.button(QDialogButtonBox.Ok).setText("确定")
        self.comboBox_3.addItems(DBField.inOutSelect)
        self.signal = update_signal

        self.first_classifier_items = settings.value(Configs.first_classifier)
        if self.first_classifier_items is None:
            self.first_classifier_items = []
        self.comboBox.addItems(self.first_classifier_items)
        self.second_classifier_items = settings.value(Configs.second_classifier)
        if self.second_classifier_items is None:
            self.second_classifier_items = []
        self.comboBox_2.addItems(self.second_classifier_items)

    def accept(self):
        db_path = settings.value(Configs.db_path)
        connect = DBOperation.get_instance(db_path)
        qdate = self.calendarWidget.selectedDate()
        date = "{}-{}-{}".format(qdate.year(), qdate.month(), qdate.day())
        inout_class = self.comboBox_3.currentText()
        first_class = self.comboBox.currentText()
        second_class = self.comboBox_2.currentText()
        price = self.lineEdit.text()
        if price != "" and check_price(price):
            connect.insert_one(date, inout_class, first_class, second_class, price)
            connect.commit()
            self.add_clear_combobox_items(first_class, second_class)
        self.signal.emit()
        self.close()

    def add_clear_combobox_items(self, first_class, second_class):
        if first_class not in self.first_classifier_items:
            self.first_classifier_items.append(first_class)
            settings.setValue(Configs.first_classifier, self.first_classifier_items)
        self.comboBox.clear()
        self.comboBox.addItems(self.first_classifier_items)
        if second_class not in self.second_classifier_items:
            self.second_classifier_items.append(second_class)
            settings.setValue(Configs.second_classifier, self.second_classifier_items)
        self.comboBox_2.clear()
        self.comboBox_2.addItems(self.second_classifier_items)
