from PyQt5.QtCore import QDateTime
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from utils.database import *

class A():
    def a(self):
        h_header = self.ui.tbvSubtaskLatest.horizontalHeader()

        # 创建表格模型(不可编辑, 默认可排序)
        self.tb_subtaskLatest_model = QtSql.QSqlTableModel(self, self.db.con)
        self.tb_subtaskLatest_model.setTable(self.tb_subtask_temp)

        # 创建选择模型
        self.selection_model_subtaskPast = QtCore.QItemSelectionModel(self.tb_subtaskLatest_model)

        # 设置表格数据模型和选择模型
        self.ui.tbvSubtaskLatest.setModel(self.tb_subtaskLatest_model)
        self.ui.tbvSubtaskLatest.setSelectionModel(self.selection_model_subtaskPast)

        # 设置表格标题
        self.subtask_latest_field_num = self.db.get_field_num(self.tb_subtaskLatest_model)  # 获取字段名和序号
        for field, column in self.subtask_latest_field_num.items():  # 设置字段显示名
            self.tb_subtaskLatest_model.setHeaderData(column, Qt.Horizontal, self.tb_subtask_header_mapping[field])
            if field not in ['register', 'class', 'sheet', 'item_no', 'description', 'mhr', 'trade']:
                self.ui.tbvSubtaskLatest.hideColumn(column)

        # 设置表格视图属性
        for field, column in self.subtask_latest_field_num.items():  # 设置表格列宽度默认行为
            if field not in ['description']:
                h_header.setSectionResizeMode(column, QtWidgets.QHeaderView.ResizeToContents)
            else:
                h_header.setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)

        # 设置表格视图的水平标题右击弹出菜单
        h_header.setContextMenuPolicy(Qt.CustomContextMenu)
        h_header.customContextMenuRequested.connect(
            lambda pos: self.show_table_header_menu(self.ui.tbvSubtaskLatest, pos))

        # 连接槽函数

        h_header.sortIndicatorChanged.connect(
            lambda index, order: self.tb_subtaskLatest_model.setSort(index,
                                                                   Qt.AscendingOrder if order else Qt.DescendingOrder))

        self.tb_subtaskLatest_model.select()