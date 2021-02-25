import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.Qt import QRect

from uis.mainwindow import Ui_MainWindow
from windows import Context, AddInfoWindow, SettingWindow, ConfirmWindow


class Wallet(QMainWindow, Ui_MainWindow):
    update_signal = pyqtSignal()
    delete_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.context = Context(self.update_signal)
        self.add_info_window = AddInfoWindow(self.update_signal)
        self.setting_window = SettingWindow()
        self.confirm_window = ConfirmWindow(self.delete_signal)
        self.del_action.triggered.connect(self.confirm_window.show)
        self.setting_action.triggered.connect(self.setting_window.show)
        self.add_action.triggered.connect(self.add_info_window.show)
        self.refresh_action.triggered.connect(self.context.reload_url)
        self.setCentralWidget(self.context)
        self.update_signal.connect(self.context.reload_url)
        # 默认窗口大小
        primary_screen_rect = QApplication.primaryScreen().geometry()
        self.default_size = QRect(int((primary_screen_rect.width() - 800) / 2) + primary_screen_rect.x(),
                                  int((primary_screen_rect.height() - 600) / 2 + primary_screen_rect.y()),
                                  800, 600)
        self.setGeometry(self.default_size)
        self.context.tableWidget.not_start = False

        # print(self.context.tableWidget.selectedItems()[0].row())
        # self.context.tableWidget.cellClicked(self.fex)

        self.delete_signal.connect(self.context.del_one_item)

    def delet(self):
        print("1")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    demo = Wallet()
    demo.show()
    sys.exit(app.exec_())
