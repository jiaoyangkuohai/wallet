import sys
import os
import traceback

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.Qt import QRect, QIcon

from uis.mainwindow import Ui_MainWindow
from windows import Context, AddInfoWindow, SettingWindow, ConfirmWindow, ConfirmExitWindow
from SingleApplication import QSingleApplication
import img


class Wallet(QMainWindow, Ui_MainWindow):
    update_signal = pyqtSignal()
    delete_signal = pyqtSignal()
    exit_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.current_dir = os.path.abspath(os.path.dirname(__file__))
        self.context = Context(self.update_signal, self.current_dir)
        self.add_info_window = AddInfoWindow(self.update_signal)
        self.setting_window = SettingWindow(self.update_signal)
        self.confirm_window = ConfirmWindow(self.delete_signal)
        self.confirm_exit_window = ConfirmExitWindow(self.exit_signal)
        self.del_action.triggered.connect(self.confirm_window.exec)
        self.setting_action.triggered.connect(self.setting_window.exec)
        self.add_action.triggered.connect(self.add_info_window.exec)
        self.refresh_action.triggered.connect(self.context.reload_url)
        self.setCentralWidget(self.context)
        self.update_signal.connect(self.context.reload_url)
        self.app = None

        # 默认窗口大小
        primary_screen_rect = QApplication.primaryScreen().geometry()
        self.default_size = QRect(int((primary_screen_rect.width() - 800) / 2) + primary_screen_rect.x(),
                                  int((primary_screen_rect.height() - 600) / 2 + primary_screen_rect.y()),
                                  800, 600)
        self.setGeometry(self.default_size)
        self.context.tableWidget.not_start = False

        self.icon = QIcon(":img/zhifu.ico")
        self.setWindowIcon(self.icon)
        self.setting_window.setWindowIcon(self.icon)
        self.add_info_window.setWindowIcon(self.icon)
        self.confirm_window.setWindowIcon(self.icon)
        self.confirm_exit_window.setWindowIcon(self.icon)


        # print(self.context.tableWidget.selectedItems()[0].row())
        # self.context.tableWidget.cellClicked(self.fex)

        self.delete_signal.connect(self.context.del_one_item)
        self.exit_signal.connect(self.closeApp)
        self._set_hotkey()

    def showMinimized(self) -> None:
        super().showMinimized()

    def _set_hotkey(self):
        """设置热键"""
        # 设置快捷键
        self.setting_action.setShortcut("F4")
        self.setting_action.setToolTip("快捷键F4")

        # 删除快捷键
        self.del_action.setShortcut("Del")
        self.del_action.setToolTip("快捷键Delete")

        # 刷新快捷键
        self.refresh_action.setShortcut("F5")
        self.refresh_action.setToolTip("快捷键F5")

        # 增加快捷键
        self.add_action.setShortcut("F6")
        self.add_action.setToolTip("快捷键F6")

    def singleton(self, mess):
        # 接受再次启动时，发送过来的信息
        if self.isHidden():
            self.show()

    def closeEvent(self, event):
        self.confirm_exit_window.show()
        event.ignore()

    def setApp(self, app):
        self.app = app

    def closeApp(self):
        self.app.quit()

def run():
    try:
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        app = QSingleApplication(sys.argv)
        try:
            if app.isRunning():
                # 发送信息
                app.sendMessage('app is running.')
                # 激活之前的窗口
                app.activateWindow()
                sys.exit(0)
            wallet = Wallet()
            app.messageReceived.connect(wallet.singleton)
            wallet.setApp(app)
            app.setActivationWindow(wallet)
            wallet.showMaximized()
            sys.exit(app.exec_())
        except Exception as e:
            traceback.print_exc()
        finally:
            app.removeServer()
    except Exception as e:
        traceback.print_exc()
    finally:
        pass


if __name__ == '__main__':
    run()
