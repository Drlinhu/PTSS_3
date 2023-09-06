import os
from pathlib import Path
import pandas as pd
from PyQt5 import QtWidgets, QtSql, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSlot, QDateTime

from ..ui import Ui_NrcReportDetailForm
from .cx_remark_dialog import CxRemarkInputDialog

from windows.image_viewer import ImageViewer
from utils.database import DatabaseManager


class NrcReportDetailWin(QtWidgets.QWidget):
    tb_subtaskPast_header_mapping = {'register': 'Register',
                                     'proj_id': 'Proj_Id',
                                     'class': 'Class',
                                     'sheet': 'Sheet',
                                     'item_no': 'Item_No',
                                     'description': 'Description',
                                     'jsn': 'Jsn',
                                     'mhr': 'Mhr',
                                     'trade': 'Trade',
                                     'report_date': 'Report_Date'
                                     }
    tb_subtaskLatest_header_mapping = {'register': 'Register',
                                       'proj_id': 'Proj_Id',
                                       'class': 'Class',
                                       'sheet': 'Sheet',
                                       'item_no': 'Item_No',
                                       'description': 'Description',
                                       'jsn': 'Jsn',
                                       'mhr': 'Mhr',
                                       'trade': 'Trade',
                                       }
    tb_cxRemark_header_mapping = {'id': 'Id',
                                  'mh_id': 'Mh_Id',
                                  'remark': 'Remark',
                                  'create_user': 'Create_User',
                                  'create_datetime': 'Create_Datetime',
                                  'update_user': 'Update_User',
                                  'update_datetime': 'Update_Datetime',
                                  }

    def __init__(self, nrc_id, parent=None):
        super(NrcReportDetailWin, self).__init__(parent)
        self.nrc_id = nrc_id
        self.db = DatabaseManager()
        self.query = QtSql.QSqlQuery(self.db.con)
        self.tb_subtask_main = "MhSubtask"
        self.tb_subtask_temp = "MhSubtaskTemp"
        self.tb_cxRemark = "MhCxRemark"

        self.ui = Ui_NrcReportDetailForm()
        self.ui.setupUi(self)
        self.setWindowTitle(f'Manhour Detail - {nrc_id}')
        self.ui.dateEditToday.setDate(QtCore.QDate.currentDate())

        # 设置past report data值
        self.ui.dateEditPast.lineEdit().setReadOnly(True)
        proj_id, jsn = self.nrc_id[:2], self.nrc_id[2:6]
        self.query.prepare(f"SELECT MAX(report_date) FROM {self.tb_subtask_main} WHERE proj_id=:proj_id AND jsn=:jsn")
        self.query.bindValue(':proj_id', proj_id)
        self.query.bindValue(':jsn', jsn)
        self.query.exec()
        if self.query.first() and self.query.value(0):
            self.ui.dateEditPast.setDate(QtCore.QDate(*[int(x) for x in self.query.value(0).split('-')]))
        else:
            self.ui.dateEditPast.setDate(QtCore.QDate.currentDate())

        # 设置description
        self.query.prepare("SELECT description FROM MhNrcReportTemp WHERE nrc_id=:nrc_id")
        self.query.bindValue(":nrc_id", self.nrc_id)
        self.query.exec()
        if self.query.first():
            self.ui.lineEditDesc.setText(self.query.value(0))

        self.init_table_subtask_past()
        self.init_table_subtask_latest()
        self.init_table_cxRemark()

        self.ui.dateEditPast.dateChanged.connect(lambda x: self.show_subtask_past_data())

    @pyqtSlot()
    def on_btnExport_clicked(self):
        today = QDateTime.currentDateTime().toString('yyyy_MM_dd_hh_mm_ss')
        filename = f'MH_CX_REMARK_{today}.xlsx'
        save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", filename, "Excel Files (*.xlsx)")
        if not save_path:
            return

        save_path = Path(save_path).resolve()
        # 创建工时记录DataFrame对象
        data = []
        header = []
        for j in range(self.tb_remark_model.columnCount()):
            header.append(self.tb_remark_model.headerData(j, Qt.Horizontal, Qt.DisplayRole))
        for i in range(self.tb_remark_model.rowCount()):
            row_data = []
            for j in range(self.tb_remark_model.columnCount()):
                row_data.append(self.tb_remark_model.data(self.tb_remark_model.index(i, j), Qt.DisplayRole))
            data.append(row_data)
        df = pd.DataFrame(data, columns=header)
        df.to_excel(save_path, index=False)
        # 打开保存文件夹
        os.startfile(save_path.parent)

    @pyqtSlot()
    def on_btnNew_clicked(self):
        dialog = CxRemarkInputDialog(mh_id=self.nrc_id)
        dialog.exec()
        self.tb_remark_model.select()

    @pyqtSlot()
    def on_btnAddImage_clicked(self):
        file_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Open Image", "",
                                                               "Image Files (*.png *.jpg *.bmp)")
        if not file_paths:
            return

        sql = """INSERT INTO MhImage
                 VALUES (:id,:mh_id,:name,:image,(SELECT IFNULL(MAX(sheet)+1,1) 
                                                  FROM MhImage 
                                                  WHERE mh_id=:mh_id))"""
        self.query.prepare(sql)
        self.db.con.transaction()  # 创建事务
        for file_path in file_paths:
            with open(file_path, 'rb') as f:
                image_data = QtCore.QByteArray(f.read())  # 以二进制模式打开图片数据并转化为QByteArray对象
            path = Path(file_path)

            self.query.bindValue(':id', None)
            self.query.bindValue(':mh_id', self.nrc_id)
            self.query.bindValue(':name', path.name)
            self.query.bindValue(':image', image_data)
            if not self.query.exec():
                QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
                self.db.con.rollback()
                return
        self.db.con.commit()
        QtWidgets.QMessageBox.information(self, 'Information', 'Successfully')

    @pyqtSlot()
    def on_btnImage_clicked(self):
        ims = []
        self.query.prepare("SELECT id,sheet,name,image FROM MhImage WHERE mh_id=:mh_id ORDER BY sheet ASC")
        self.query.bindValue(':mh_id', self.nrc_id)
        self.query.exec()
        while self.query.next():
            ims.append({field: self.query.value(field) for field in ['id', 'sheet', 'name', 'image']})
        if not ims:
            QtWidgets.QMessageBox.information(self, 'Information', 'No images')
            return

        self.image_viewer = ImageViewer('MhImage', ims)
        self.image_viewer.show()
        self.image_viewer.fit_image()

    @pyqtSlot()
    def on_btnDelete_clicked(self):
        sel_model = self.selection_model_remark
        selected_indexes = sel_model.selectedRows(column=self.remark_field_num['id'])
        if not selected_indexes:
            QtWidgets.QMessageBox.information(self, 'Information', 'No row(s) selected!')
            return
        choose = QtWidgets.QMessageBox.warning(self, 'Warning', 'Are you sure to delete?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choose == QtWidgets.QMessageBox.Yes:
            self.query.prepare(f"""DELETE FROM {self.tb_cxRemark} WHERE id=:id""")
            self.db.con.transaction()
            for index in selected_indexes:
                self.query.bindValue(':id', index.data())
                if not self.query.exec():
                    QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text(), )
                    self.db.con.rollback()  # 回滚事务
                    return
            self.db.con.commit()
            QtWidgets.QMessageBox.information(self, 'Information', 'Deleted!')
            self.tb_remark_model.select()

    def on_tbvCxRemark_doubleClicked(self, index: QtCore.QModelIndex):
        row = index.row()
        data = {'id_': self.tb_remark_model.index(row, self.remark_field_num['id']).data(),
                'mh_id': self.tb_remark_model.index(row, self.remark_field_num['mh_id']).data(),
                'remark': self.tb_remark_model.index(row, self.remark_field_num['remark']).data(),
                'ct_user': self.tb_remark_model.index(row, self.remark_field_num['create_user']).data(),
                'ct_dt': self.tb_remark_model.index(row, self.remark_field_num['create_datetime']).data(),
                'up_user': self.tb_remark_model.index(row, self.remark_field_num['update_user']).data(),
                'up_dt': self.tb_remark_model.index(row, self.remark_field_num['update_datetime']).data(), }

        dialog = CxRemarkInputDialog(**data, ignore_text_changed=True)
        dialog.exec()
        self.tb_remark_model.select()

    def init_table_subtask_past(self):
        h_header = self.ui.tbvSubtaskPast.horizontalHeader()

        # 创建表格模型(不可编辑, 默认可排序)
        self.tb_subtaskPast_model = QtSql.QSqlTableModel(self, self.db.con)
        self.tb_subtaskPast_model.setTable(self.tb_subtask_main)

        # 创建选择模型
        self.selection_model_subtaskPast = QtCore.QItemSelectionModel(self.tb_subtaskPast_model)

        # 设置表格数据模型和选择模型
        self.ui.tbvSubtaskPast.setModel(self.tb_subtaskPast_model)
        self.ui.tbvSubtaskPast.setSelectionModel(self.selection_model_subtaskPast)

        # 设置表格标题
        self.subtask_past_field_num = self.db.get_field_num(self.tb_subtaskPast_model)  # 获取字段名和序号
        for field, column in self.subtask_past_field_num.items():  # 设置字段显示名
            self.tb_subtaskPast_model.setHeaderData(column, Qt.Horizontal, self.tb_subtaskPast_header_mapping[field])
            if field not in ['register', 'class', 'sheet', 'item_no', 'description', 'mhr', 'trade', 'report_date']:
                self.ui.tbvSubtaskPast.hideColumn(column)

            if field not in ['description']:
                h_header.setSectionResizeMode(column, QtWidgets.QHeaderView.ResizeToContents)
            else:
                h_header.setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)

        # 设置表格视图的水平标题右击弹出菜单
        h_header.setContextMenuPolicy(Qt.CustomContextMenu)
        h_header.customContextMenuRequested.connect(
            lambda pos: self.show_table_header_menu(self.ui.tbvSubtaskPast, pos))

        self.show_subtask_past_data()

    def init_table_subtask_latest(self):
        h_header = self.ui.tbvSubtaskLatest.horizontalHeader()

        # 创建表格模型(不可编辑, 默认可排序)
        self.tb_subtaskLatest_model = QtSql.QSqlTableModel(self, self.db.con)
        self.tb_subtaskLatest_model.setTable(self.tb_subtask_temp)

        # 创建选择模型
        self.selection_model_subtaskLatest = QtCore.QItemSelectionModel(self.tb_subtaskLatest_model)

        # 设置表格数据模型和选择模型
        self.ui.tbvSubtaskLatest.setModel(self.tb_subtaskLatest_model)
        self.ui.tbvSubtaskLatest.setSelectionModel(self.selection_model_subtaskLatest)

        # 设置表格标题
        self.subtask_past_field_num = self.db.get_field_num(self.tb_subtaskLatest_model)  # 获取字段名和序号
        for field, column in self.subtask_past_field_num.items():  # 设置字段显示名
            self.tb_subtaskLatest_model.setHeaderData(column, Qt.Horizontal,
                                                      self.tb_subtaskLatest_header_mapping[field])
            if field not in ['register', 'class', 'sheet', 'item_no', 'description', 'mhr', 'trade']:
                self.ui.tbvSubtaskLatest.hideColumn(column)

            if field not in ['description']:
                h_header.setSectionResizeMode(column, QtWidgets.QHeaderView.ResizeToContents)
            else:
                h_header.setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)

        # 设置表格视图的水平标题右击弹出菜单
        h_header.setContextMenuPolicy(Qt.CustomContextMenu)
        h_header.customContextMenuRequested.connect(
            lambda pos: self.show_table_header_menu(self.ui.tbvSubtaskLatest, pos))

        # 显示数据
        proj_id, jsn = self.nrc_id[:2], self.nrc_id[2:6]
        filter_str = f"""proj_id='{proj_id}' AND jsn='{jsn}' ORDER BY item_no ASC"""
        self.tb_subtaskLatest_model.setFilter(filter_str)
        self.tb_subtaskLatest_model.select()

    def init_table_cxRemark(self):
        h_header = self.ui.tbvCxRemark.horizontalHeader()

        # 创建表格模型(不可编辑, 默认可排序)
        self.tb_remark_model = QtSql.QSqlTableModel(self, self.db.con)
        self.tb_remark_model.setTable(self.tb_cxRemark)

        # 创建选择模型
        self.selection_model_remark = QtCore.QItemSelectionModel(self.tb_remark_model)

        # 设置表格数据模型和选择模型
        self.ui.tbvCxRemark.setModel(self.tb_remark_model)
        self.ui.tbvCxRemark.setSelectionModel(self.selection_model_remark)

        # 设置表格标题
        self.remark_field_num = self.db.get_field_num(self.tb_remark_model)  # 获取字段名和序号
        for field, column in self.remark_field_num.items():  # 设置字段显示名
            self.tb_remark_model.setHeaderData(column, Qt.Horizontal, self.tb_cxRemark_header_mapping[field])

        # 设置表格视图属性
        for field, column in self.remark_field_num.items():  # 设置表格列宽度默认行为
            if field not in ['remark']:
                h_header.setSectionResizeMode(column, QtWidgets.QHeaderView.ResizeToContents)
            else:
                h_header.setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)
            if field in ['id']:
                self.ui.tbvCxRemark.hideColumn(column)

        # 设置表格视图的水平标题右击弹出菜单
        h_header.setContextMenuPolicy(Qt.CustomContextMenu)
        h_header.customContextMenuRequested.connect(lambda pos: self.show_table_header_menu(self.ui.tbvCxRemark, pos))

        self.tb_remark_model.setFilter(f"mh_id='{self.nrc_id}'")
        self.tb_remark_model.select()

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

    def show_subtask_past_data(self):
        # 显示数据
        proj_id, jsn = self.nrc_id[:2], self.nrc_id[2:6]
        past_dt = self.ui.dateEditPast.date().toString('yyyy-MM-dd')
        filter_str = f"""proj_id='{proj_id}' AND jsn='{jsn}' AND report_date='{past_dt}' ORDER BY item_no ASC"""
        self.tb_subtaskPast_model.setFilter(filter_str)
        self.tb_subtaskPast_model.select()
