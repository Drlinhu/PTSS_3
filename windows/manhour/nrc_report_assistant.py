import os
from pathlib import Path
import pandas as pd
from PyQt5 import QtWidgets, QtSql, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSlot, QDateTime

from ..ui import Ui_NrcReprotAssistantForm
from windows.image_viewer import ImageViewer
from windows.input_date_dialog import DateInputDialog
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
                        'mh_changed': 'MH_Changed'
                        }

CELL_BG = {}


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
        self.tbReport_model = NrcReportSqlTableModel(self, self.db.con)
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
    def on_pushButtonSearch_clicked(self):  # TODO
        self.tbReport_model.select()

    @pyqtSlot()
    def on_btnReportImport_clicked(self):
        def get_history_report_mh(nrc_id):
            self.query.prepare(f"SELECT total FROM {self.table_main} WHERE nrc_id=:nrc_id")
            self.query.bindValue(':nrc_id', nrc_id)
            self.query.exec()
            if self.query.first():
                return self.query.value('total')
            return 0.0

        read_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, filter="Excel Files (*.xlsx)")
        if not read_path:
            return

        """导入NRC工时记录"""
        # 验证数据字段完整性
        df = pd.read_excel(read_path, nrows=0)
        for x in TABLE_HEADER_MAPPING.values():
            if x not in df.columns:
                QtWidgets.QMessageBox.critical(self, 'Error', f'Column `{x}` not found in excel!')
                return
        # 读取并保存数据
        converters = {
            'Description': lambda y: str(y).strip(),
            'ATA': lambda y: str(y),
            'Total': lambda y: f'{y:.2f}',
            'MH_Changed': lambda y: f'{y:.2f}',
        }
        df = pd.read_excel(read_path, keep_default_na=False, converters=converters)
        header_mh_changed = TABLE_HEADER_MAPPING['mh_changed']
        header_total = TABLE_HEADER_MAPPING['total']
        header_nrcId = TABLE_HEADER_MAPPING['nrc_id']
        for i in range(df.shape[0]):
            old_total = float(get_history_report_mh(df.loc[i, header_nrcId]))
            new_total = float(df.loc[i, header_total])
            df.loc[i, header_mh_changed] = f'{new_total - old_total:.2f}'

        sql = f"""REPLACE INTO {self.table_temp}
                  VALUES ({','.join(['?' for _ in range(self.tbReport_model.columnCount())])})"""
        self.query.prepare(sql)
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
            QtWidgets.QMessageBox.information(self, 'Information', 'Import NRC successfully!')
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
        self.query.prepare("SELECT id,sheet,name,image FROM MhImage WHERE mh_id=:mh_id ORDER BY sheet ASC")
        self.query.bindValue(':mh_id', mh_id)
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
    def on_btnReportDetail_clicked(self):  # TODO
        pass

    @pyqtSlot()
    def on_btnReportSubtask_clicked(self):  # TODO
        pass

    @pyqtSlot()
    def on_btnReportSave_clicked(self):  # TODO
        # 打开日期输入日期窗口
        dialog = DateInputDialog()
        dialog.set_label('Input report date:')
        dialog.exec()
        report_date = dialog.date()
        # 将temp表的内容存入到正式数据库表中
        sql = f"""REPLACE INTO {self.table_main} 
                                (nrc_id,register,ref_task,description,area,trade,ata,status,standard,total,report_date) 
                    SELECT nrc_id,register,ref_task,description,area,trade,ata,status,standard,total,:dt 
                    FROM {self.table_temp};
                 """
        self.query.prepare(sql)
        self.query.bindValue(':dt', report_date)
        if not self.query.exec():
            QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
        else:
            QtWidgets.QMessageBox.information(self, 'Information', 'Saved')
            self.query.exec("DELETE FROM MhNrcReportTemp")
            self.tbReport_model.select()

    @pyqtSlot()
    def on_btnHistoryExport_clicked(self):  # TODO
        pass

    @pyqtSlot()
    def on_btnHistoryImage_clicked(self):  # TODO
        pass

    @pyqtSlot()
    def on_btnHistoryDetail_clicked(self):  # TODO
        pass

    @pyqtSlot()
    def on_btnHistorySubtask_clicked(self):  # TODO
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

    def mark_report_difference(self):

        sql = f"""SELECT * 
                  FROM {self.table_main} 
                  WHERE nrc_id=:nrc_id AND report_date=(SELECT MAX(report_date) 
                                                        FROM {self.table_main} WHERE nrc_id=:nrc_id)
               """
        self.query.prepare(sql)
        for row in range(self.tbReport_model.rowCount()):
            nrc_id = self.tbReport_model.index(row, self.field_num['nrc_id']).data(Qt.DisplayRole)
            self.query.bindValue(':nrc_id', nrc_id)
            self.query.exec()
            if self.query.first():  # 真表示已存在记录，则比较和存在的记录是否相同
                print(self.query.value('nrc_id'))
            else:  # 数据库不存在，表明为新的记录
                pass


class NrcReportSqlTableModel(QtSql.QSqlTableModel):
    def __init__(self, parent, QObject=None, *args, **kwargs):
        super().__init__(parent, QObject, *args, **kwargs)

    def data(self, index, role=Qt.DisplayRole):
        sql = f"""SELECT *
                  FROM MhNrcReport
                  WHERE nrc_id=:nrc_id AND report_date=(SELECT MAX(report_date)
                                                        FROM MhNrcReport WHERE nrc_id=:nrc_id)
               """
        query = self.query()
        query.prepare(sql)
        if role == Qt.BackgroundRole:
            nrc_id = self.data(self.index(index.row(), self.fieldIndex('nrc_id')), Qt.DisplayRole)
            value = index.data(Qt.DisplayRole)
            field_name = self.fieldIndex(self.headerData(index.column(), Qt.Horizontal, Qt.DisplayRole))
            query.bindValue(':nrc_id', nrc_id)
            query.exec_()
            # 根据条件设置行背景颜色，只要有个不同整行显示黄色
            if query.first() and value != query.value(field_name) and index.column() != self.fieldIndex('mh_changed'):
                CELL_BG[index.row()] = QtGui.QColor(255, 255, 0)
                return QtGui.QColor(255, 255, 0)  # 黄色
            else:
                return QtGui.QColor(255, 255, 255)  # 白色

        if role == Qt.TextColorRole:
            value = index.data(Qt.DisplayRole)
            if index.column() == self.fieldIndex('mh_changed') and value != 0:
                return QtGui.QColor(255, 0, 0)  # 红色

        return super().data(index, role)
