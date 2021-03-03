from PyQt5.QtWidgets import QDialogButtonBox, QDialog
from PyQt5.QtCore import pyqtSignal

from uis.confirm_exit import Ui_Dialog


class ConfirmExitWindow(QDialog, Ui_Dialog):
    def __init__(self, exit_signal: pyqtSignal):
        super().__init__()
        self.setupUi(self)
        self.exit_signal = exit_signal
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("取消")
        self.buttonBox.button(QDialogButtonBox.Ok).setText("确定")

    def accept(self):
        self.exit_signal.emit()
        self.close()
