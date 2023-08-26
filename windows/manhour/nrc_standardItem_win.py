import os
from pathlib import Path
import pandas as pd
from PyQt5 import QtWidgets, QtSql, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSlot, QDateTime

from ..ui import Ui_NrcStandardForm
from windows.image_viewer import ImageViewer
from utils.database import DatabaseManager


class NrcStandardItemWin(QtWidgets.QWidget):
    tb_header_mapping = {'item_no': 'Item_NO',
                         'ac_type': 'AC_Type',
                         'description': 'Description',
                         'work_area': 'Work_Area'}

    def __init__(self, parent=None):
        super(NrcStandardItemWin, self).__init__(parent)
        self.is_saved = True
        self.db = DatabaseManager()
        self.query = QtSql.QSqlQuery(self.db.con)
        self.tb_item_name = 'MhNrcStandardItem'
        self.tb_item_max = 'MhNrcStandardMax'
        self.tb_item_min = 'MhNrcStandardMin'
        self.tb_item_remark = 'MhNrcStandardRemark'
        self.tb_item_image = 'MhNrcStandardRemark'

        self.ui = Ui_NrcStandardForm()
        self.ui.setupUi(self)
        self.init_table()

    @pyqtSlot()
    def on_btnSearch_clicked(self):  # TODO
        pass

    @pyqtSlot()
    def on_btnImport_clicked(self):  # TODO
        pass

    @pyqtSlot()
    def on_btnExport_clicked(self):  # TODO
        pass

    @pyqtSlot()
    def on_btnNew_clicked(self):  # TODO
        pass

    @pyqtSlot()
    def on_btnAddImage_clicked(self):  # TODO
        pass

    @pyqtSlot()
    def on_btnImage_clicked(self):  # TODO
        pass

    @pyqtSlot()
    def on_btnDelete_clicked(self):  # TODO
        pass

    @pyqtSlot()
    def on_btnSave_clicked(self):  # TODO
        pass

    def init_table(self):
        h_header = self.ui.tbvNrcItem.horizontalHeader()

        # 创建表格模型(不可编辑, 默认可排序)
        self.model = QtSql.QSqlTableModel(self, self.db.con)
        self.model.setTable(self.tb_item_name)

        # 创建选择模型
        self.selection_model = QtCore.QItemSelectionModel(self.model)

        # 设置表格数据模型和选择模型
        self.ui.tbvNrcItem.setModel(self.model)
        self.ui.tbvNrcItem.setSelectionModel(self.selection_model)

        # 设置表格标题
        self.field_num = self.db.get_field_num(self.model)  # 获取字段名和序号
        for field, column in self.field_num.items():  # 设置字段显示名
            self.model.setHeaderData(column, Qt.Horizontal, self.tb_header_mapping[field])

        # 设置表格视图属性
        for field, column in self.field_num.items():  # 设置表格列宽度默认行为
            if field in ['description']:
                h_header.setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)
            else:
                h_header.setSectionResizeMode(column, QtWidgets.QHeaderView.ResizeToContents)
            if field in ['item_no', 'work_area']:
                self.ui.tbvNrcItem.hideColumn(column)

        # 设置表格视图的水平标题右击弹出菜单
        h_header.setContextMenuPolicy(Qt.CustomContextMenu)
        h_header.customContextMenuRequested.connect(lambda pos: self.show_table_header_menu(self.ui.tbvNrcItem, pos))

        # 连接槽函数

        h_header.sortIndicatorChanged.connect(
            lambda index, order: self.model.setSort(index,
                                                    Qt.AscendingOrder if order else Qt.DescendingOrder))

    def show_table_header_menu(self, table: QtWidgets.QTableView, pos):
        h_header = table.horizontalHeader()
        # 创建右键菜单
        menu = QtWidgets.QMenu(self)
        # 获取右键点击处的列索引
        column = h_header.logicalIndexAt(pos)
        # 添加菜单项
        if h_header.sectionResizeMode(column) == QtWidgets.QHeaderView.Interactive:
            column_resizable_action = QtWidgets.QAction("Non-resizable", self)
        else:
            column_resizable_action = QtWidgets.QAction("Resizable", self)
        column_resizable_action.triggered.connect(lambda: self.set_column_resizable(h_header, pos))
        menu.addAction(column_resizable_action)

        # 显示右键菜单
        menu.exec_(table.viewport().mapToGlobal(pos))

    @classmethod
    def set_column_resizable(cls, header, pos):
        # 获取右键点击处的列索引
        column = header.logicalIndexAt(pos)
        if header.sectionResizeMode(column) == QtWidgets.QHeaderView.Interactive:
            header.setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)
        else:
            header.setSectionResizeMode(column, QtWidgets.QHeaderView.Interactive)
