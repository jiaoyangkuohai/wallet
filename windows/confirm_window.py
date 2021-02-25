from PyQt5.QtWidgets import QDialogButtonBox, QDialog
from PyQt5.QtCore import pyqtSignal

from uis.confirm import Ui_Dialog


class ConfirmWindow(QDialog, Ui_Dialog):
    def __init__(self, delete_signal: pyqtSignal):
        super().__init__()
        self.setupUi(self)
        self.delete_signal = delete_signal
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("取消")
        self.buttonBox.button(QDialogButtonBox.Ok).setText("确定")

    def accept(self):
        self.delete_signal.emit()
        self.close()
