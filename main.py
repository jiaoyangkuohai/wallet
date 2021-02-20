import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.Qt import QRect

from context_window import Context


class Wallet(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setCentralWidget(Context())

        # 默认窗口大小
        primary_screen_rect = QApplication.primaryScreen().geometry()
        self.default_size = QRect(int((primary_screen_rect.width() - 800) / 2) + primary_screen_rect.x(),
                                  int((primary_screen_rect.height() - 600) / 2 + primary_screen_rect.y()),
                                  800, 600)
        self.setGeometry(self.default_size)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Wallet()
    demo.show()
    sys.exit(app.exec_())
