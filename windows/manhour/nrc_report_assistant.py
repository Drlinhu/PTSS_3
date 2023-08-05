import os
from pathlib import Path
import pandas as pd
from PyQt5 import QtWidgets, QtSql, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSlot, QDateTime

from ..ui import Ui_NrcReprotAssistantForm
from windows.image_viewer import ImageViewer
from utils.database import DatabaseManager
from utils.nrc_corpus import *

TABLE_HEADER_MAPPING = {'nrc_id': 'Nrc_Id',
                        'register': 'Register',
                        'ref_task': 'Ref_Task',
                        'description': 'Description',
                        'area': 'Area',
                        'trade': 'Trade',
                        'ata': 'ATA',
                        'status': 'Status',
                        'standard': 'Standard',
                        'total': 'Total',
                        }


class NrcReportAssistantWin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(NrcReportAssistantWin, self).__init__(parent)
        self.ui = Ui_NrcReprotAssistantForm()
        self.ui.setupUi(self)

        self.table_main = "MhNrcReport"
        self.table_temp = "MhNrcReportTemp"
        self.db = DatabaseManager()
        self.query = QtSql.QSqlQuery(self.db.con)

        self.init_table()

    def init_table(self):  # 初始化表格
        self.tbReport_hHeader = self.ui.tableViewReport.horizontalHeader()

        # 创建表格模型(不可编辑, 默认可排序)
        self.tbReport_model = QtSql.QSqlTableModel(self, self.db.get_connection_by_name())
        self.tbReport_model.setTable(self.table_temp)

        # 创建选择模型
        self.selection_model = QtCore.QItemSelectionModel(self.tbReport_model)

        # 设置表格数据模型和选择模型
        self.ui.tableViewReport.setModel(self.tbReport_model)
        self.ui.tableViewReport.setSelectionModel(self.selection_model)

        # 设置表格标题
        self.field_num = self.db.get_field_num(self.tbReport_model)  # 获取字段名和序号
        for field, column in self.field_num.items():  # 设置字段显示名
            self.tbReport_model.setHeaderData(column, Qt.Horizontal, TABLE_HEADER_MAPPING[field])

        # 设置表格视图属性
        for field, column in self.field_num.items():  # 设置表格列宽度默认行为
            if field not in ['description', 'total']:
                self.tbReport_hHeader.setSectionResizeMode(column, QtWidgets.QHeaderView.ResizeToContents)
            else:
                self.tbReport_hHeader.setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)

        # 设置表格视图的水平标题右击弹出菜单
        self.tbReport_hHeader.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tbReport_hHeader.customContextMenuRequested.connect(self.show_table_header_menu)

        # 连接槽函数

        self.tbReport_hHeader.sortIndicatorChanged.connect(
            lambda index, order: self.tbReport_model.setSort(index, Qt.AscendingOrder if order else Qt.DescendingOrder))

        self.tbReport_model.select()

    @pyqtSlot()
    def on_pushButtonSearch_clicked(self):
        self.tbReport_model.select()

    @pyqtSlot()
    def on_btnReportImport_clicked(self):
        read_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, filter="Excel Files (*.xlsx)")
        if not read_path:
            return

        df = pd.read_excel(read_path, nrows=0)
        # 验证数据字段完整性
        for x in TABLE_HEADER_MAPPING.values():
            if x not in df.columns:
                QtWidgets.QMessageBox.critical(self, 'Error', f'Column `{x}` not found in excel!')
                return
        # 读取并保存数据
        converters = {
            'Description': lambda y: str(y).strip(),
            'ATA': lambda y: str(y),
            'Total': lambda y: f'{y:.2f}',
        }
        df = pd.read_excel(read_path, keep_default_na=False, converters=converters)

        self.query.prepare(f"""REPLACE INTO {self.table_temp}
                               VALUES ({','.join(['?' for _ in range(self.tbReport_model.columnCount())])})""")
        fault = False  # 标记在保存到数据库中是否存在错误
        self.db.con.transaction()
        for i in range(df.shape[0]):
            for field, column in self.field_num.items():
                header = TABLE_HEADER_MAPPING[field]
                self.query.addBindValue(df.loc[i, header])
            if not self.query.exec_():
                fault = True
                break
        if not fault:  # 如果存入数据库无错误则直接提交否则退回之前的操作
            self.db.con.commit()
            QtWidgets.QMessageBox.information(self, 'Information', 'Import successfully!')
            self.tbReport_model.select()
        else:
            self.db.con.rollback()

    @pyqtSlot()
    def on_btnReportExport_clicked(self):
        today = QDateTime.currentDateTime().toString('yyyy_MM_dd_hh_mm_ss')
        filename = f'MH_NRC_Report_{today}.xlsx'
        save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", filename, "Excel Files (*.xlsx)")
        if not save_path:
            return

        save_path = Path(save_path).resolve()
        data = []
        header = []
        for j in range(self.tbReport_model.columnCount()):
            header.append(self.tbReport_model.headerData(j, Qt.Horizontal, Qt.DisplayRole))
        for i in range(self.tbReport_model.rowCount()):
            row_data = []
            for j in range(self.tbReport_model.columnCount()):
                print(self.tbReport_model.data(self.tbReport_model.index(i, j), Qt.DisplayRole))
                row_data.append(self.tbReport_model.data(self.tbReport_model.index(i, j), Qt.DisplayRole))
            data.append(row_data)
        df = pd.DataFrame(data, columns=header)
        df.to_excel(save_path, index=False)
        os.startfile(save_path.cwd())

    @pyqtSlot()
    def on_btnReportAddImage_clicked(self):
        model = self.ui.tableViewReport.selectionModel()
        selected_rowIndexes = model.selectedRows(column=self.field_num['nrc_id'])
        if not selected_rowIndexes:
            QtWidgets.QMessageBox.information(self, 'Information', 'No row(s) selected!')
            return

        file_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Open Image", "",
                                                               "Image Files (*.png *.jpg *.bmp)")
        if not file_paths:
            return

        sql = """INSERT INTO MhImage
                 VALUES (:id,:nrc_id,:name,:image,(SELECT IFNULL(MAX(sheet)+1,1) FROM MhImage WHERE mh_id=:nrc_id))"""
        self.db.con.transaction()  # 创建事务
        fault = False
        self.query.prepare(sql)
        for file_path in file_paths:
            with open(file_path, 'rb') as f:
                image_data = QtCore.QByteArray(f.read())  # 以二进制模式打开图片数据并转化为QByteArray对象
            path = Path(file_path)
            for index in selected_rowIndexes:
                self.query.bindValue(':id', None)
                self.query.bindValue(':nrc_id', index.data())
                self.query.bindValue(':name', path.name)
                self.query.bindValue(':image', image_data)
                if not self.query.exec():
                    fault = True
                    print(self.query.executedQuery())
                    break
            if fault:
                break
        if not fault:
            self.db.con.commit()
            QtWidgets.QMessageBox.information(self, 'Information', 'Successfully')
        else:
            QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())

    @pyqtSlot()
    def on_btnReportImage_clicked(self):
        model = self.ui.tableViewReport.selectionModel()
        selected_rowIndexes = model.selectedRows(column=self.field_num['nrc_id'])
        if len(selected_rowIndexes) != 1:
            QtWidgets.QMessageBox.information(self, 'Information', 'One row should be selected!')
            return
        ims = []
        mh_id = selected_rowIndexes[0].data()
        self.query.prepare("SELECT sheet,name,image FROM MhImage WHERE mh_id=:mh_id ORDER BY sheet ASC")
        self.query.bindValue(':mh_id', mh_id)
        self.query.exec()
        while self.query.next():
            ims.append({field: self.query.value(field) for field in ['sheet', 'name', 'image']})
        if not ims:
            QtWidgets.QMessageBox.information(self, 'Information', 'No images')
            return

        self.image_viewer = ImageViewer('MhImage', ims)
        self.image_viewer.show()

    @pyqtSlot()
    def on_btnReportDetail_clicked(self):
        pass

    @pyqtSlot()
    def on_btnReportSubtask_clicked(self):
        pass

    @pyqtSlot()
    def on_btnReportSave_clicked(self):
        pass

    @pyqtSlot()
    def on_btnHistoryExport_clicked(self):
        pass

    @pyqtSlot()
    def on_btnHistoryImage_clicked(self):
        pass

    @pyqtSlot()
    def on_btnHistoryDetail_clicked(self):
        pass

    @pyqtSlot()
    def on_btnHistorySubtask_clicked(self):
        pass

    def show_table_header_menu(self, pos):
        # 创建右键菜单
        menu = QtWidgets.QMenu(self)
        # 获取右键点击处的列索引
        column = self.tbReport_hHeader.logicalIndexAt(pos)
        # 添加菜单项
        if self.tbReport_hHeader.sectionResizeMode(column) == QtWidgets.QHeaderView.Interactive:
            column_resizable_action = QtWidgets.QAction("Non-resizable", self)
        else:
            column_resizable_action = QtWidgets.QAction("Resizable", self)
        column_resizable_action.triggered.connect(lambda: self.set_column_resizable(pos))
        menu.addAction(column_resizable_action)

        # 显示右键菜单
        menu.exec_(self.ui.tableViewReport.viewport().mapToGlobal(pos))

    def set_column_resizable(self, pos):
        # 获取右键点击处的列索引
        column = self.tbReport_hHeader.logicalIndexAt(pos)

        if self.tbReport_hHeader.sectionResizeMode(column) == QtWidgets.QHeaderView.Interactive:
            self.tbReport_hHeader.setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)
        else:
            self.tbReport_hHeader.setSectionResizeMode(column, QtWidgets.QHeaderView.Interactive)
