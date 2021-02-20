import os
import numpy as np
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.Qt import QUrl, QFileInfo
from uis.context import Ui_Form

from database import DBOperation
from mytest.mypies import render_df_html


class Context(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.splitter.setSizes([200, 130])
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
        print(self.scrollArea.geometry())
        print(self.view.geometry())
        # self.index = './data/template.html'
        # self.index = "./mytest/render.html"
        # self.index = "./mytest/pie_set_color.html"
        # self.index = "./mytest/pie_base.html"
        self.index = "./pie_base.html"
        # self.index = "./mytest/multiple_pie.html"
        html_path = QFileInfo(self.index).absoluteFilePath()
        print(html_path)
        self.url = QUrl("file:///"+html_path)
        self.view.load(self.url)
        self.scrollArea.setWidget(self.view)



