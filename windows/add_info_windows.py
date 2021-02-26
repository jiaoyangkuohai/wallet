from PyQt5.QtWidgets import QDialogButtonBox, QDialog

from uis.add_info import Ui_Dialog
from database import DBOperation, DBField


class AddInfoWindow(QDialog, Ui_Dialog):
    def __init__(self, update_signal):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("取消")
        self.buttonBox.button(QDialogButtonBox.Ok).setText("确定")
        self.comboBox_3.addItems(DBField.inOutSelect)
        self.signal = update_signal

    def accept(self):
        connect = DBOperation.get_instance()
        qdate = self.calendarWidget.selectedDate()
        date = "{}-{}-{}".format(qdate.year(), qdate.month(), qdate.day())
        inout_class = self.comboBox_3.currentText()
        first_class = self.comboBox.currentText()
        second_class = self.comboBox_2.currentText()
        price = self.lineEdit.text()
        if price != "":
            connect.insert_one(date, inout_class, first_class, second_class, price)
            connect.commit()
        self.signal.emit()
        self.close()
