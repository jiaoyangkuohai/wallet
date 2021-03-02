import os
import numpy as np
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.Qt import QUrl, QFileInfo
from uis.context import Ui_Form

from database import DBOperation
from render_html import render_df_html
from utils import settings, Configs


class Context(QWidget, Ui_Form):
    def __init__(self, update_signal, main_path):
        super().__init__()
        self.setupUi(self)
        self.main_path = main_path
        self.splitter.setSizes([200, 300])
        self.update_signal = update_signal
        self.tableWidget.set_signal(update_signal)
        # self._init_table()
        self.df = self.tableWidget.load_data_from_db()
        self._web_init()

    def _web_init(self):
        render_df_html(self.df)
        self.view = QWebEngineView()
        # self.scrollArea.setWidget(self.view)
        # todo 尺寸修改
        # self.view.resize(self.label.width(), self.label.height())
        # print(self.scrollAreaWidgetContents.geometry())
        # self.view.setGeometry(self.scrollAreaWidgetContents.geometry())
        self.view.resize(800, 800)
        # print(self.scrollArea.geometry())
        # print(self.view.geometry())
        # self.index = './data/template.html'
        # self.index = "./mytest/render.html"
        # self.index = "./mytest/pie_set_color.html"
        # self.index = "./mytest/pie_base.html"
        self.index = "./pie_base.html"
        # self.index = "./template.html"
        # self.index = "./mytest/multiple_pie.html"
        html_path = QFileInfo(self.index).absoluteFilePath()
        # print(html_path)
        self.url = QUrl("file:///"+html_path)
        self.view.load(self.url)
        self.scrollArea.setWidget(self.view)

    def reload_url(self):
        self.tableWidget.not_start = True
        self.df = self.tableWidget.load_data_from_db()
        render_df_html(self.df)
        # 高分屏自适应
        html_path = "./pie_base.html"
        html_path = QFileInfo(html_path).absoluteFilePath()
        self.url = QUrl("file:///" + html_path)
        self.view.load(self.url)

    def del_one_item(self):
        num = len(self.tableWidget.selectedItems())
        if num == 0:
            pass
        else:
            db_path = settings.value(Configs.db_path)
            connect = DBOperation.get_instance(db_path)
            # print(self.tableWidget.selectedItems()[0].row())
            # print(self.tableWidget.selectedItems()[0].text())
            row_num = self.tableWidget.selectedItems()[0].row()
            id = self.tableWidget.item(row_num, 0).text()
            # print("id: {}".format(id))
            connect.delete_one(id)
            connect.commit()
            self.update_signal.emit()

