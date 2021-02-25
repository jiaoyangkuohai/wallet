import pandas as pd
import numpy as np
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView, QMenu
import traceback

from database import DBOperation


class TableWidget(QTableWidget):  # 1
    def __init__(self, parent):
        super(TableWidget, self).__init__(parent=parent)
        self.db = DBOperation()
        # self.cellClicked.connect(self.get_row)
        # self.itemClicked.connect(self.get_row)
        self.not_start = True
        self.itemChanged.connect(self.update_database)
        self.signal = None


        # 右键菜单
        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.del_menu)
        # self._init_menu()
        # 双击修改
        self.setEditTriggers(QAbstractItemView.DoubleClicked)

    def set_signal(self, signal):
        self.signal = signal

    def _init_menu(self):
        self.menu_action = QMenu()
        self.menu_action.addAction("删除")

    def load_data_to_table(self):
        """
        将数据放到表中进行展示
        :return:
        """
        # self.parent = parent
        self.setRowCount(6)  # 2
        self.setColumnCount(5)
        # self.table = QTableWidget(6, 6, self)

        print(self.rowCount())  # 3
        print(self.columnCount())

        self.setColumnWidth(0, 60)  # 4
        self.setRowHeight(0, 30)

        classifier = ['日期', '大类', '小类', '支出', '收入']
        self.setHorizontalHeaderLabels(classifier)  # 5

        self.setVerticalHeaderLabels(['t1', 't2', 't3', 't4', 't5', 't6'])

        # self.setShowGrid(False)                       # 6

        self.item_1 = QTableWidgetItem('2020-10-03')  # 7
        self.setItem(0, 0, self.item_1)

        self.item_2 = QTableWidgetItem('Bye')  # 8
        self.item_2.setTextAlignment(Qt.AlignCenter)
        self.setItem(2, 2, self.item_2)

        self.setSpan(2, 2, 2, 2)  # 9

        print(self.findItems('Hi', Qt.MatchExactly))  # 10
        print(self.findItems('B', Qt.MatchContains))

    def update_database(self, item: QTableWidgetItem):
        """
        更新数据库
        """
        print("进入数据库更新: {}, {}".format(item.row(), item.column()))
        if self.not_start:
            print("not start")
            return
        try:
            # print(item.row(), item.column())
            # print(item.text())
            # row_index = self.selectedItems()[0].row()
            # print(self.item(item.row(), 0).text())
            connect = DBOperation.get_instance()
            row_num = item.row()
            id = self.item(row_num, 0).text()
            date = self.item(row_num, 1).text()
            first_class = self.item(row_num, 2).text()
            second_class = self.item(row_num, 3).text()
            price = self.item(row_num, 4).text()
            connect.update_one(id, date, first_class, second_class, price)
            connect.commit()
            self.signal.emit()
        except Exception as e:
            traceback.print_exc()

    def del_menu(self, pos):
        self.menu_action.exec_(self.mapToGlobal(pos))

    def get_row(self):
        try:
            row_index = self.selectedItems()[0].row()
            print(row_index, self.item(row_index, 0).text())
        except Exception as e:
            print(e)




    def load_data_from_db(self):
        """
        从数据库中获取数据
        :return:
        """
        df: pd.DataFrame = self.db.search_all()
        row_num, col_num = df.shape
        self.setRowCount(row_num)
        self.setColumnCount(col_num)

        classifier = ['id', '日期', '大类', '小类', '收入\支出']
        self.setHorizontalHeaderLabels(classifier)
        # 隐藏id
        self.setColumnHidden(0, True)

        for i in range(row_num):
            input_table_rows_values = df.iloc[[i]]
            input_table_rows_values_array = np.array(input_table_rows_values)
            input_table_rows_values_list = input_table_rows_values_array.tolist()[0]

            for j in range(col_num):
                input_table_items_list = input_table_rows_values_list[j]

                input_table_items = str(input_table_items_list)
                newItem = QTableWidgetItem(input_table_items)
                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.setItem(i, j, newItem)

        self.not_start = False
        return df
