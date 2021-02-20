import pandas as pd
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem

from database import DBOperation


class TableWidget(QTableWidget):  # 1
    def __init__(self, parent):
        super(TableWidget, self).__init__(parent=parent)
        self.db = DBOperation()

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
        self.setColumnHidden(0, True)

        for i in range(row_num):
            input_table_rows_values = df.iloc[[i]]
            input_table_rows_values_array = np.array(input_table_rows_values)
            input_table_rows_values_list = input_table_rows_values_array.tolist()[0]

            for j in range(col_num):
                input_table_items_list = input_table_rows_values_list[j]

                input_table_items = str(input_table_items_list)
                newItem = QTableWidgetItem(input_table_items)
                newItem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.setItem(i, j, newItem)
        return df
