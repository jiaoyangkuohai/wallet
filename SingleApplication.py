# -*- coding: utf-8 -*-
"""
@Time : 2020/2/5 15:56
@Author : SHIHONGLIANG
@File : SingleApplication.py
"""
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtNetwork import QLocalSocket, QLocalServer
from PyQt5.QtWidgets import QApplication

class QSingleApplication(QApplication):
    # https://github.com/PyQt5/PyQt/blob/master/Demo/Lib/Application.py
    messageReceived = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        # logger.debug("{} init...".format(self.__class__.__name__))
        super(QSingleApplication, self).__init__(*args, **kwargs)
        # 使用路径作为appid
        # appid = QApplication.applicationFilePath().lower().split("/")[-1]
        # 使用固定的appid
        appid = "SHL_LHX_Wallet"
        # logger.debug("{} appid name: {}".format(self.__class__.__name__,appid))
        # self._socketName = "qtsingleapp-" + appid
        self._socketName = appid
        # print("socketName", self._socketName)
        self._activationWindow = None
        self._activateOnMessage = False
        self._socketServer = None
        self._socketIn = None
        self._socketOut = None
        self._running = False

        # 先尝试连接
        self._socketOut = QLocalSocket(self)
        self._socketOut.connectToServer(self._socketName)
        self._socketOut.error.connect(self.handleError)
        self._running = self._socketOut.waitForConnected()
        # logger.debug("local socket connect error: {}".format(self._socketOut.errorString()))

        if not self._running:  # 程序未运行
            # logger.debug("start init QLocalServer.")
            self._socketOut.close()
            del self._socketOut
            self._socketServer = QLocalServer(self)
            # 设置连接权限
            self._socketServer.setSocketOptions(QLocalServer.UserAccessOption)
            self._socketServer.listen(self._socketName)
            self._socketServer.newConnection.connect(self._onNewConnection)
            self.aboutToQuit.connect(self.removeServer)
            # logger.debug("QLocalServer finished init.")

    def handleError(self, message):
        print("handleError message: ", message)

    def isRunning(self):
        return self._running

    def activationWindow(self):
        return self._activationWindow

    def setActivationWindow(self, activationWindow, activateOnMessage=True):
        self._activationWindow = activationWindow
        self._activateOnMessage = activateOnMessage

    def activateWindow(self):
        if not self._activationWindow:
            return
        self._activationWindow.setWindowState(
            self._activationWindow.windowState() & ~Qt.WindowMinimized)
        self._activationWindow.raise_()
        self._activationWindow.activateWindow()
        # 增加了显示功能。
        # self._activationWindow.show()

    def sendMessage(self, message, msecs=5000):
        if not self._socketOut:
            return False
        if not isinstance(message, bytes):
            message = str(message).encode()
        self._socketOut.write(message)
        if not self._socketOut.waitForBytesWritten(msecs):
            raise RuntimeError("Bytes not written within %ss" %
                               (msecs / 1000.))
        return True

    def _onNewConnection(self):
        if self._socketIn:
            self._socketIn.readyRead.disconnect(self._onReadyRead)
        self._socketIn = self._socketServer.nextPendingConnection()
        if not self._socketIn:
            return
        self._socketIn.readyRead.connect(self._onReadyRead)
        if self._activateOnMessage:
            self.activateWindow()

    def _onReadyRead(self):
        while 1:
            message = self._socketIn.readLine()
            if not message:
                break
            # print("Message received: ", message)
            self.messageReceived.emit(message.data().decode())

    def removeServer(self):
        if self._socketServer is not None:
            self._socketServer.close()
            self._socketServer.removeServer(self._socketName)