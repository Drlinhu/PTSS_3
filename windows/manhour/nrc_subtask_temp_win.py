import os
from pathlib import Path
import pandas as pd
from PyQt5 import QtWidgets, QtSql
from PyQt5.QtCore import Qt, pyqtSlot, QDateTime

from ..ui import Ui_SubtaskForm
from utils.database import DatabaseManager


class NrcSubtaskTempWin(QtWidgets.QWidget):
    table_header_mapping = {'register': 'Register',
                            'proj_id': 'Proj_Id',
                            'class': 'Class',
                            'sheet': 'Sheet',
                            'item_no': 'Item_No',
                            'description': 'Description',
                            'jsn': 'Jsn',
                            'mhr': 'Mhr',
                            'trade': 'Trade',
                            }

    def __init__(self, nrc_id, parent=None, ):
        super(NrcSubtaskTempWin, self).__init__(parent)
        self.table_name = "MhSubtaskTemp"
        self.db = DatabaseManager()
        self.query = self.db.con
        self.nrc_id = nrc_id
        proj_id, jsn = self.nrc_id[:2], self.nrc_id[2:6]
        self.filter_str = f"""proj_id='{proj_id}' AND jsn='{jsn}' ORDER BY item_no ASC"""

        self.ui = Ui_SubtaskForm()
        self.ui.setupUi(self)
        self.setWindowTitle(f'Subtasks - {self.nrc_id}')

        # 初始化表格
        self.init_table()

    @pyqtSlot()
    def on_btnReportExport_clicked(self):
        today = QDateTime.currentDateTime().toString('yyyy_MM_dd_hh_mm_ss')
        filename = f'MH_NRC_Subtask_{today}.xlsx'
        save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", filename, "Excel Files (*.xlsx)")
        if not save_path:
            return

        save_path = Path(save_path).resolve()
        # 创建工时记录DataFrame对象
        data = []
        header = []
        for j in range(self.model.columnCount()):
            header.append(self.model.headerData(j, Qt.Horizontal, Qt.DisplayRole))
        for i in range(self.model.rowCount()):
            row_data = []
            for j in range(self.model.columnCount()):
                row_data.append(self.model.data(self.model.index(i, j), Qt.DisplayRole))
            data.append(row_data)
        df = pd.DataFrame(data, columns=header)
        df.to_excel(save_path, index=False)
        # 打开保存文件夹
        os.startfile(save_path.parent)

    def init_table(self):
        self.h_header = self.ui.tableView.horizontalHeader()

        # 创建数据模型
        self.model = QtSql.QSqlTableModel(self, self.db.con)
        self.model.setTable(self.table_name)
        self.model.setFilter(self.filter_str)
        self.model.select()

        # 设置表格数据模型
        self.ui.tableView.setModel(self.model)

        # 设置表格标题
        self.field_num = self.db.get_field_num(self.model)  # 获取字段名和序号
        for field, column in self.field_num.items():
            self.model.setHeaderData(column, Qt.Horizontal, self.table_header_mapping[field])
            if field not in ['register', 'class', 'sheet', 'item_no', 'description', 'mhr', 'trade']:
                self.ui.tableView.hideColumn(column)

            if field not in ['description']:
                self.h_header.setSectionResizeMode(column, QtWidgets.QHeaderView.ResizeToContents)
            else:
                self.h_header.setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)

        # 设置表格视图右击弹出菜单
        self.h_header.setContextMenuPolicy(Qt.CustomContextMenu)  # 表格标题
        self.h_header.customContextMenuRequested.connect(self.show_table_header_menu)

        # 槽函数
        self.h_header.sortIndicatorChanged.connect(
            lambda index, order: self.model.setSort(index, Qt.AscendingOrder if order else Qt.DescendingOrder))

    def show_table_header_menu(self, pos):
        # 创建右键菜单
        menu = QtWidgets.QMenu(self)
        # 获取右键点击处的列索引
        column = self.h_header.logicalIndexAt(pos)
        # 添加菜单项
        if self.h_header.sectionResizeMode(column) == QtWidgets.QHeaderView.Interactive:
            column_resizable_action = QtWidgets.QAction("Non-resizable", self)
        else:
            column_resizable_action = QtWidgets.QAction("Resizable", self)
        column_resizable_action.triggered.connect(lambda: self.set_column_resizable(pos))
        menu.addAction(column_resizable_action)

        # 显示右键菜单
        menu.exec_(self.ui.tableView.viewport().mapToGlobal(pos))

    def set_column_resizable(self, pos):
        # 获取右键点击处的列索引
        column = self.h_header.logicalIndexAt(pos)

        if self.h_header.sectionResizeMode(column) == QtWidgets.QHeaderView.Interactive:
            self.h_header.setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)
        else:
            self.h_header.setSectionResizeMode(column, QtWidgets.QHeaderView.Interactive)
