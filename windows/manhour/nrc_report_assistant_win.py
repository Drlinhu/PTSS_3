import os
from pathlib import Path
import pandas as pd
from PyQt5 import QtWidgets, QtSql, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSlot, QDateTime

from ..ui import Ui_NrcReprotAssistantForm
from .mh_finalized_detail_win import ManhourFinalizedWin
from .mh_subtask_win import TABLE_HEADER_MAPPING as subtask_header_mapping
from .nrc_subtask_temp_win import NrcSubtaskTempWin
from .nrc_report_detail_win import NrcReportDetailWin
from .nrc_manhour_trend import NrcManhourTrendWin
from windows.image_viewer import ImageViewer
from windows.input_date_dialog import DateInputDialog
from utils.database import DatabaseManager
from utils.nrc_corpus import *

TABLE_HEADER_MAPPING = {'nrc_id': 'NRC_ID',
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
        self.table_main = "MhNrcReport"
        self.table_temp = "MhNrcReportTemp"
        self.db = DatabaseManager()
        self.query = QtSql.QSqlQuery(self.db.con)

        self.ui = Ui_NrcReprotAssistantForm()
        self.ui.setupUi(self)
        self.ui.comboBoxTrade.addItems(['', 'AE', 'AV', 'AI', 'SM', 'PT', 'SS', 'CL', 'GW', ])
        self.ui.comboBoxStatus.addItems(['', 'WIP', 'OPEN', 'COMP', ])
        self.ui.comboBoxStandard.addItems(['', 'Y', 'N'])

        self.init_report_table()
        self.init_history_table()
        self.show_report_summary()

    def init_report_table(self):  # 初始化表格
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
            if field not in ['description']:
                self.tbReport_hHeader.setSectionResizeMode(column, QtWidgets.QHeaderView.ResizeToContents)
            else:
                self.tbReport_hHeader.setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)

        # 设置表格视图的水平标题右击弹出菜单
        self.tbReport_hHeader.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tbReport_hHeader.customContextMenuRequested.connect(self.show_table_header_menu)

        # 连接槽函数
        self.tbReport_hHeader.sortIndicatorChanged.connect(
            lambda index, order: self.tbReport_model.setSort(index, Qt.AscendingOrder if order else Qt.DescendingOrder))
        self.ui.lineEditNrcId.returnPressed.connect(self.on_btnSearch_clicked)
        self.ui.lineEditRefTask.returnPressed.connect(self.on_btnSearch_clicked)
        self.ui.lineEditArea.returnPressed.connect(self.on_btnSearch_clicked)
        self.ui.lineEditDesc.returnPressed.connect(self.on_btnSearch_clicked)
        self.ui.comboBoxRegister.lineEdit().returnPressed.connect(self.on_btnSearch_clicked)

        # 显示数据
        self.tbReport_model.select()

    def init_history_table(self):
        header_labels = ['MH_ID', 'Register', 'Description', 'Total', 'Simis']
        self.ui.tableWidgetHistory.setColumnCount(len(header_labels))
        self.ui.tableWidgetHistory.setHorizontalHeaderLabels(header_labels)

        h_header = self.ui.tableWidgetHistory.horizontalHeader()
        for col, field in enumerate(header_labels):
            if field in ['Description']:
                h_header.setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)
            else:
                h_header.setSectionResizeMode(col, QtWidgets.QHeaderView.ResizeToContents)

    @pyqtSlot(bool)
    def on_checkBoxAll_clicked(self, checked):
        if checked:
            self.ui.checkBoxNew.setChecked(False)
            self.ui.checkBoxChanged.setChecked(False)

    @pyqtSlot(bool)
    def on_checkBoxNew_clicked(self, checked):
        if checked:
            self.ui.checkBoxAll.setChecked(False)
            self.ui.checkBoxChanged.setChecked(False)

    @pyqtSlot(bool)
    def on_checkBoxChanged_clicked(self, checked):
        if checked:
            self.ui.checkBoxAll.setChecked(False)
            self.ui.checkBoxNew.setChecked(False)

    @pyqtSlot()
    def on_btnSearch_clicked(self):
        # self.table_main = "MhNrcReport"
        # self.table_temp = "MhNrcReportTemp"
        condition = {}
        if self.ui.lineEditNrcId.text():
            condition['nrc_id'] = self.ui.lineEditNrcId.text()
        if self.ui.comboBoxRegister.currentText():
            condition['register'] = self.ui.comboBoxRegister.currentText()
        if self.ui.comboBoxTrade.currentText():
            condition['trade'] = self.ui.comboBoxTrade.currentText()
        if self.ui.lineEditArea.text():
            condition['area'] = self.ui.lineEditArea.text()
        if self.ui.lineEditDesc.text():
            condition['description'] = self.ui.lineEditDesc.text()
        if self.ui.comboBoxStatus.currentText():
            condition['status'] = self.ui.comboBoxStatus.currentText()
        if self.ui.comboBoxStandard.currentText():
            condition['standard'] = self.ui.comboBoxStandard.currentText()
        if self.ui.lineEditRefTask.text():
            condition['ref_task'] = self.ui.lineEditRefTask.text()

        filter_str = ' AND '.join([f"{field} LIKE '%{value}%'" for field, value in condition.items()])
        nrc_id = []
        if self.ui.checkBoxNew.isChecked():

            sql = f"""SELECT DISTINCT t1.nrc_id
                      FROM {self.table_temp} AS t1
                      LEFT JOIN {self.table_main} AS t2 ON t2.nrc_id = t1.nrc_id
                      WHERE report_date IS NULL"""
            self.query.exec(sql)
            while self.query.next():
                nrc_id.append(self.query.value('nrc_id'))
        elif self.ui.checkBoxChanged.isChecked():
            fields = ['nrc_id', 'register', 'ref_task', 'description', 'area', 'trade', 'ata', 'status', 'standard',
                      'total', ]
            sql = f"""SELECT t1.nrc_id,MAX(report_date)
                      FROM {self.table_temp} AS t1
                      JOIN {self.table_main} AS t2 ON t2.nrc_id = t1.nrc_id
                      WHERE {' OR '.join([f't1.{field}!=t2.{field}' for field in fields])}
                      GROUP BY t1.nrc_id"""
            self.query.exec(sql)
            while self.query.next():
                nrc_id.append(self.query.value('nrc_id'))
        else:
            pass

        if nrc_id and filter_str:
            filter_str += ' AND (' + ' OR '.join([f'nrc_id={nrc_id}' for nrc_id in nrc_id]) + ')'
        elif nrc_id and not filter_str:
            filter_str = ' OR '.join([f"nrc_id='{nrc_id}'" for nrc_id in nrc_id])
        else:
            pass

        self.tbReport_model.setFilter(filter_str)
        self.tbReport_model.select()

    @pyqtSlot()
    def on_btnReportImport_clicked(self):
        def get_history_report_mh(nrc_id):
            sql_ = f"""SELECT total FROM {self.table_main} 
                       WHERE nrc_id=:nrc_id AND report_date=(SELECT MAX(report_date) 
                                                             FROM {self.table_main} 
                                                             WHERE nrc_id=:nrc_id)"""
            self.query.prepare(sql_)
            self.query.bindValue(':nrc_id', nrc_id)
            self.query.exec()
            if self.query.first():
                return self.query.value('total')
            return 0.0

        read_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, filter="Excel Files (*.xlsx)")
        if not read_path:
            return

        # 读取整个Excel文件
        xlsx = pd.ExcelFile(read_path)
        """ 验证文件 """

        sheet_header = {'NRC': TABLE_HEADER_MAPPING.values(),
                        'Subtask': subtask_header_mapping.values()}

        for sheet_name, header in sheet_header.items():
            if sheet_name not in xlsx.sheet_names:  # 验证页面是否存在
                QtWidgets.QMessageBox.critical(self, 'Error', f'Sheet `{sheet_name}` not found in excel!')
                return

            df_nrc = pd.read_excel(xlsx, sheet_name=sheet_name, nrows=0)
            for x in header:  # 验证数据字段完整性
                if x not in df_nrc.columns:
                    msg = f'Column `{x}` not found in {sheet_name} sheet!'
                    QtWidgets.QMessageBox.critical(self, 'Error', msg)
                    return

        # 读取NRC
        converters = {
            'Description': lambda y: str(y).strip(),
            'ATA': lambda y: str(y),
            'Total': lambda y: f'{y:.2f}',
            'MH_Changed': lambda y: f'{y:.2f}',
        }
        df_nrc = pd.read_excel(xlsx, sheet_name='NRC', keep_default_na=False, converters=converters)
        header_mh_changed = TABLE_HEADER_MAPPING['mh_changed']
        header_total = TABLE_HEADER_MAPPING['total']
        header_nrcId = TABLE_HEADER_MAPPING['nrc_id']
        for i in range(df_nrc.shape[0]):
            old_total = float(get_history_report_mh(df_nrc.loc[i, header_nrcId]))
            new_total = float(df_nrc.loc[i, header_total])
            df_nrc.loc[i, header_mh_changed] = f'{new_total - old_total:.2f}'

        # 读取Subtask
        converters = {
            'Description': lambda y: str(y).strip(),
            'Item_No': lambda y: str(y),
            'Mhr': lambda y: f'{y:.2f}',
        }
        df_subtask = pd.read_excel(xlsx, sheet_name='Subtask', keep_default_na=False, converters=converters)

        fault = False  # 标记在保存到数据库中是否存在错误
        # 保存NRC到数据库中
        self.db.con.transaction()
        sql = f"""REPLACE INTO {self.table_temp}
                  VALUES ({','.join(['?' for _ in range(self.tbReport_model.columnCount())])})"""
        self.query.prepare(sql)
        for i in range(df_nrc.shape[0]):
            for field, column in self.field_num.items():
                header = TABLE_HEADER_MAPPING[field]
                self.query.addBindValue(df_nrc.loc[i, header])
            if not self.query.exec_():
                fault = True
                break
        if fault:
            self.db.con.rollback()
            QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
            return

        sql = f"""REPLACE INTO MhSubtaskTemp 
                 VALUES ({','.join(['?' for _ in range(len(subtask_header_mapping))])})"""
        self.query.prepare(sql)
        for i in range(df_subtask.shape[0]):
            for header in subtask_header_mapping.values():
                self.query.addBindValue(df_subtask.loc[i, header])
            if not self.query.exec_():
                fault = True
                break
        if fault:
            self.db.con.rollback()
            QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
            return

        # 若没有错误，则提交数据
        self.db.con.commit()
        QtWidgets.QMessageBox.information(self, 'Information', 'Import successfully!')
        self.tbReport_model.select()
        self.show_report_summary()

    @pyqtSlot()
    def on_btnReportExport_clicked(self):
        today = QDateTime.currentDateTime().toString('yyyy_MM_dd_hh_mm_ss')
        filename = f'MH_NRC_Report_{today}.xlsx'
        save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", filename, "Excel Files (*.xlsx)")
        if not save_path:
            return

        save_path = Path(save_path).resolve()

        # 创建NRC工时DataFrame对象
        data = []
        header = []
        for j in range(self.tbReport_model.columnCount()):
            header.append(self.tbReport_model.headerData(j, Qt.Horizontal, Qt.DisplayRole))
        for i in range(self.tbReport_model.rowCount()):
            row_data = []
            for j in range(self.tbReport_model.columnCount()):
                row_data.append(self.tbReport_model.data(self.tbReport_model.index(i, j), Qt.DisplayRole))
            data.append(row_data)
        df_nrc = pd.DataFrame(data, columns=header)

        # 创建subtaskDataFrame对象
        self.query.exec("SELECT * FROM MhSubtaskTemp")
        data = []
        header = [subtask_header_mapping[self.query.record().fieldName(i)] for i in range(self.query.record().count())]
        while self.query.next():
            record = [self.query.value(i) for i in range(self.query.record().count())]
            data.append(record)
        df_subtask = pd.DataFrame(data, columns=header)

        # 创建Excel Writer对象
        writer = pd.ExcelWriter(save_path)
        # 将DataFrame对象写入Excel文件中的不同工作表
        df_nrc.to_excel(writer, sheet_name='NRC', index=False)
        df_subtask.to_excel(writer, sheet_name='Subtask', index=False)
        # 保存Excel文件
        writer.close()
        # 打开保存文件夹
        os.startfile(save_path.parent)

    @pyqtSlot()
    def on_btnReportDelete_clicked(self):
        sel_model = self.selection_model
        selected_indexes = sel_model.selectedRows(column=self.field_num['nrc_id'])
        if not selected_indexes:
            QtWidgets.QMessageBox.information(self, 'Information', 'No row(s) selected!')
            return
        choose = QtWidgets.QMessageBox.warning(self, 'Warning', 'Are you sure to delete?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choose == QtWidgets.QMessageBox.Yes:
            self.db.con.transaction()
            # 删除NRC temp
            self.query.prepare(f"""DELETE FROM {self.table_temp} WHERE nrc_id=:nrc_id""")

            for index in selected_indexes:
                self.query.bindValue(':nrc_id', index.data())
                if not self.query.exec():
                    QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text(), )
                    self.db.con.rollback()  # 回滚事务
                    return
            # 删除NRC对应的SUBTASK
            self.query.prepare(f"""DELETE FROM MhSubtaskTemp WHERE proj_id=:proj_id AND jsn=:jsn""")
            for index in selected_indexes:
                nrc_id = index.data()
                proj_id, jsn = nrc_id[:2], nrc_id[2:6]
                self.query.bindValue(':proj_id', proj_id)
                self.query.bindValue(':jsn', jsn)
                if not self.query.exec():
                    QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text(), )
                    self.db.con.rollback()  # 回滚事务

            self.db.con.commit()
            QtWidgets.QMessageBox.information(self, 'Information', 'Deleted!')
            self.tbReport_model.select()

    @pyqtSlot()
    def on_btnReportAddImage_clicked(self):
        sel_model = self.ui.tableViewReport.selectionModel()
        sel_rowIndexes = sel_model.selectedRows(column=self.field_num['nrc_id'])
        if not sel_rowIndexes:
            QtWidgets.QMessageBox.information(self, 'Information', 'No row(s) selected!')
            return

        file_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Open Image", "",
                                                               "Image Files (*.png *.jpg *.bmp)")
        if not file_paths:
            return

        sql = """INSERT INTO MhImage
                 VALUES (:id,:nrc_id,:name,:image,(SELECT IFNULL(MAX(sheet)+1,1) FROM MhImage WHERE mh_id=:nrc_id))"""
        self.db.con.transaction()  # 创建事务
        self.query.prepare(sql)
        for file_path in file_paths:
            with open(file_path, 'rb') as f:
                image_data = QtCore.QByteArray(f.read())  # 以二进制模式打开图片数据并转化为QByteArray对象
            path = Path(file_path)
            for index in sel_rowIndexes:
                self.query.bindValue(':id', None)
                self.query.bindValue(':nrc_id', index.data())
                self.query.bindValue(':name', path.name)
                self.query.bindValue(':image', image_data)
                if not self.query.exec():
                    self.db.con.rollback()
                    QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
                    return
        self.db.con.commit()
        QtWidgets.QMessageBox.information(self, 'Information', 'Successfully')

    @pyqtSlot()
    def on_btnReportImage_clicked(self):
        sel_model = self.ui.tableViewReport.selectionModel()
        sel_rowIndexes = sel_model.selectedRows(column=self.field_num['nrc_id'])
        if len(sel_rowIndexes) != 1:
            QtWidgets.QMessageBox.information(self, 'Information', 'One row should be selected!')
            return
        ims = []
        mh_id = sel_rowIndexes[0].data()
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
    def on_btnReportDetail_clicked(self):
        model = self.ui.tableViewReport.selectionModel()
        selected_rowIndexes = model.selectedRows(column=self.field_num['nrc_id'])
        if len(selected_rowIndexes) != 1:
            QtWidgets.QMessageBox.information(self, 'Information', 'One row should be selected!')
            return
        nrc_id = selected_rowIndexes[0].data()
        self.report_detail = NrcReportDetailWin(nrc_id)
        self.report_detail.show()

    @pyqtSlot()
    def on_btnReportSubtask_clicked(self):
        sel_model = self.ui.tableViewReport.selectionModel()
        selected_rowIndexes = sel_model.selectedRows(column=self.field_num['nrc_id'])
        if len(selected_rowIndexes) != 1:
            QtWidgets.QMessageBox.information(self, 'Information', 'One row should be selected!')
            return
        nrc_id = selected_rowIndexes[0].data()
        self.subtask_win = NrcSubtaskTempWin(nrc_id)
        self.subtask_win.show()

    @pyqtSlot()
    def on_btnReportCalenderCheck_clicked(self):
        self.nrc_trend_win = NrcManhourTrendWin()
        self.nrc_trend_win.show()

    @pyqtSlot()
    def on_btnReportSave_clicked(self):
        if self.tbReport_model.rowCount() < 1:
            return

        # 打开日期输入日期窗口
        dialog = DateInputDialog()
        dialog.set_label('Input report date:')
        if not dialog.exec():
            return
        report_date = dialog.date()
        mode = dialog.model()

        fault = False
        self.db.con.transaction()

        # 将reportTemp表的内容存入到正式表中
        sql = f"""{mode} INTO {self.table_main} 
                                (nrc_id,register,ref_task,description,area,trade,ata,status,standard,total,report_date) 
                    SELECT nrc_id,register,ref_task,description,area,trade,ata,status,standard,total,:dt 
                    FROM {self.table_temp};
                 """
        self.query.prepare(sql)
        self.query.bindValue(':dt', report_date)
        if not self.query.exec():
            fault = True
            QtWidgets.QMessageBox.critical(self, 'Error', 'Save NRC failed:\n' + self.query.lastError().text())
        if fault:
            self.db.con.rollback()
            return

        # 将subtaskTemp表内容存入到正式表中
        sql = f"""{mode} INTO MhSubtask SELECT *,:dt FROM MhSubtaskTemp"""
        self.query.prepare(sql)
        self.query.bindValue(':dt', report_date)
        if not self.query.exec():
            fault = True
            QtWidgets.QMessageBox.critical(self, 'Error', 'Save Subtask failed:\n' + self.query.lastError().text())
        if fault:
            self.db.con.rollback()
            return

        self.db.con.commit()
        QtWidgets.QMessageBox.information(self, 'Information', 'Saved')
        self.query.exec("DELETE FROM MhNrcReportTemp")
        self.query.exec("DELETE FROM MhSubtaskTemp")
        self.tbReport_model.select()

    @pyqtSlot()
    def on_btnHistoryExport_clicked(self):
        today = QDateTime.currentDateTime().toString('yyyy_MM_dd_hh_mm_ss')
        filename = f'MH_Similarity_{today}.xlsx'
        save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", filename, "Excel Files (*.xlsx)")
        if not save_path:
            return

        save_path = Path(save_path).resolve()

        data = []
        table = self.ui.tableWidgetHistory
        header = [table.horizontalHeaderItem(i).data(Qt.DisplayRole) for i in range(table.columnCount())]
        for i in range(table.rowCount()):
            temp = [
                float(table.item(i, j).data(Qt.DisplayRole)) if j in [3, 4] else table.item(i, j).data(Qt.DisplayRole)
                for j in range(table.columnCount())]
            data.append(temp)

        df = pd.DataFrame(data, columns=header)
        df.to_excel(save_path, index=False)
        # 打开保存文件夹
        os.startfile(save_path.parent)

    @pyqtSlot()
    def on_btnHistoryImage_clicked(self):
        sel_model = self.ui.tableWidgetHistory.selectionModel()
        sel_rowIndexes = sel_model.selectedRows(column=0)
        if len(sel_rowIndexes) != 1:
            QtWidgets.QMessageBox.information(self, 'Information', 'One row should be selected!')
            return
        ims = []
        mh_id = sel_rowIndexes[0].data()
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
    def on_btnHistoryDetail_clicked(self):
        sel_model = self.ui.tableWidgetHistory.selectionModel()
        if len(sel_model.selectedRows(0)) != 1:
            QtWidgets.QMessageBox.information(self, 'Information', 'One row should be selected!')
            return
        mh_id = sel_model.selectedIndexes()[0].data()
        self.query.prepare("SELECT * FROM MhFinalized WHERE mh_id=:mh_id")
        self.query.bindValue(':mh_id', mh_id)
        self.query.exec()
        self.query.first()
        data = {self.query.record().fieldName(i): self.query.value(i) for i in range(self.query.record().count())}
        self.detail_win = ManhourFinalizedWin()
        self.detail_win.setData(**data)
        self.detail_win.show()

    @pyqtSlot()
    def on_btnHistorySubtask_clicked(self):
        sel_model = self.ui.tableWidgetHistory.selectionModel()
        sel_rowIndexes = sel_model.selectedRows(column=self.field_num['nrc_id'])
        if len(sel_rowIndexes) != 1:
            QtWidgets.QMessageBox.information(self, 'Information', 'One row should be selected!')
            return
        nrc_id = sel_rowIndexes[0].data()
        self.subtask_win = NrcSubtaskTempWin(nrc_id)
        self.subtask_win.show()

    def on_tableViewReport_doubleClicked(self, index: QtCore.QModelIndex):
        row = index.row()
        desc = self.tbReport_model.index(row, self.field_num['description']).data()
        sims = self.ui.doubleSpinBoxSim.value()
        show_count = self.ui.spinBoxHistoryRows.value()
        corpus = ManhourVectorCorpus()
        results = corpus.get_similarity_by_latest(search_text=desc, threshold=sims, show_count=show_count)

        # 根据获得结果的位置，进一步查询数据库
        data = []
        sql = f"SELECT mh_id,register,description,total FROM MhFinalized LIMIT 1 OFFSET :offset"
        self.query.prepare(sql)
        for r in results:
            self.query.bindValue(":offset", r[0])
            if self.query.exec() and self.query.first():
                data.append([self.query.value(i) for i in range(4)] + [f'{r[1]:.2f}'])

        if not data:
            QtWidgets.QMessageBox.information(self, 'Information', 'No similar history data.')
            return
        # 将数据显示在history表格中
        history_table = self.ui.tableWidgetHistory
        history_table.setRowCount(len(data))
        for i in range(history_table.rowCount()):
            for j in range(history_table.columnCount()):
                item = QtWidgets.QTableWidgetItem(str(data[i][j]))
                history_table.setItem(i, j, item)

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

    def show_report_summary(self):
        # self.table_main = "MhNrcReport"
        # self.table_temp = "MhNrcReportTemp"

        # 读取当前report工时总额
        sql = f""" SELECT SUM(total) FROM {self.table_temp} """
        self.query.exec(sql)
        self.query.first()
        cur_total = self.query.value(0) if self.query.value(0) else 0

        # 获取机号和对应的Project ID
        self.query.exec(f"SELECT nrc_id,register FROM {self.table_temp} LIMIT 1")
        if self.query.first():
            proj_id = self.query.value('nrc_id')[:2]
            register = self.query.value('register')

            # 读取report历史最新日期的工时总额
            sql = f""" SELECT SUM(total) 
                       FROM {self.table_main}
                       WHERE register=:register AND nrc_id LIKE :proj_id AND report_date=(
                                                                SELECT MAX(report_date) 
                                                                FROM {self.table_main}
                                                                WHERE register=:register AND nrc_id LIKE :proj_id)"""
            self.query.prepare(sql)
            self.query.bindValue(':register', register)
            self.query.bindValue(':proj_id', proj_id + '%')
            self.query.exec()
            self.query.first()
            last_total = self.query.value(0) if self.query.value(0) else 0
        else:
            last_total = 0

        # 显示数据
        self.ui.lineEditTotalCurrent.setText(f'{cur_total:.2f}')
        self.ui.lineEditTotalLast.setText(f'{last_total:.2f}')
        changed_total = cur_total - last_total
        self.ui.lineEditTotalChanged.setText(f'{changed_total:.2f}')
        if changed_total > 0:
            self.ui.lineEditTotalChanged.setStyleSheet("background-color: #FFC0CB;")  # pink
        else:
            self.ui.lineEditTotalChanged.setStyleSheet("background-color: #90EE90;")  # light green


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
            if query.first():
                if value != query.value(field_name) and index.column() != self.fieldIndex('mh_changed'):
                    CELL_BG[index.row()] = QtGui.QColor(255, 255, 0)
                    return QtGui.QColor(255, 255, 0)  # 黄色
                else:
                    return QtGui.QColor(255, 255, 255)  # 白色
            else:
                return QtGui.QColor(127, 255, 0)  # 绿色 新增

        if role == Qt.TextColorRole:
            value = index.data(Qt.DisplayRole)
            if index.column() == self.fieldIndex('mh_changed'):
                if value > 0:
                    return QtGui.QColor(255, 0, 0)  # 红色
                elif value < 0:
                    return QtGui.QColor(0, 255, 0)  # 绿色
                else:
                    return QtGui.QColor(0, 0, 0)  # 黑色

        return super().data(index, role)
