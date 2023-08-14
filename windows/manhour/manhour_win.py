import os
from pathlib import Path
import pandas as pd
from PyQt5 import QtWidgets, QtSql, QtCore
from PyQt5.QtCore import pyqtSlot, Qt, QDateTime, QItemSelectionModel

from ..ui.ui_manhourform import Ui_ManHourForm
from ..image_viewer import ImageViewer
from .mh_finalized_detail_win import ManhourFinalizedWin
from .nrc_subtask_temp_win import NrcSubtaskTempWin
from .nrc_report_assistant_win import NrcReportAssistantWin
from .nrc_manhour_trend import NrcManhourTrendWin
from utils.database import DatabaseManager
from utils.nrc_corpus import *

TABLE_HEADER_MAPPING = {'mh_id': 'MH_Id',
                        'class': 'Class',
                        'pkg_id': 'Pkg_Id',
                        'wo': 'WO',
                        'ac_type': 'Ac_Type',
                        'register': 'Register',
                        'ref_task': 'Ref_Task',
                        'description': 'Description',
                        'trade': 'Trade',
                        'ata': 'ATA',
                        'area': 'Area',
                        'zone': 'Zone',
                        'category': 'Category',
                        'skill': 'Skill',
                        'unskill': 'Unskill',
                        'total': 'Total',
                        'standard': 'Standard',
                        'dskill': 'D_Skill',
                        'dunskill': 'D_Unskill',
                        'dtotal': 'D_Total',
                        'remark': 'Remark',
                        }


class ManhourWin(QtWidgets.QWidget):
    progress_signal = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(ManhourWin, self).__init__(parent)
        self.ui = Ui_ManHourForm()
        self.ui.setupUi(self)

        self.table_name = "MhFinalized"
        self.db = DatabaseManager()
        self.query = QtSql.QSqlQuery(self.db.con)

        self.init_table()  # 初始化表格

    def init_table(self):

        # 创建表格模型(不可编辑, 默认可排序)
        self.table_model = QtSql.QSqlTableModel(self, self.db.get_connection_by_name())
        self.table_model.setTable(self.table_name)

        # 创建选择模型
        self.selection_model = QItemSelectionModel(self.table_model)

        # 设置表格数据模型和选择模型
        self.ui.tableView.setModel(self.table_model)
        self.ui.tableView.setSelectionModel(self.selection_model)

        # 设置表格标题
        self.field_num = self.db.get_field_num(self.table_model)  # 获取字段名和序号
        for field, column in self.field_num.items():  # 设置字段显示名
            self.table_model.setHeaderData(column, Qt.Horizontal, TABLE_HEADER_MAPPING[field])

        # 设置表格视图属性
        for field, column in self.field_num.items():  # 设置表格列宽度默认行为
            if field not in ['description', 'remark']:
                self.ui.tableView.horizontalHeader().setSectionResizeMode(column,
                                                                          QtWidgets.QHeaderView.ResizeToContents)
            else:
                self.ui.tableView.horizontalHeader().setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)

        # 设置表格视图的水平标题右击弹出菜单
        self.ui.tableView.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableView.horizontalHeader().customContextMenuRequested.connect(self.show_table_header_menu)

        # 连接槽函数
        self.ui.tableView.horizontalHeader().sortIndicatorChanged.connect(
            lambda index, order: self.table_model.setSort(index, Qt.AscendingOrder if order else Qt.DescendingOrder))

    @pyqtSlot()
    def on_toolButtonNrcReportAssistant_clicked(self):
        self.nrc_reportAssistant_win = NrcReportAssistantWin()
        self.nrc_reportAssistant_win.show()

    @pyqtSlot()
    def on_toolButtonNrcMhTrend_clicked(self):
        self.nrc_trend_win = NrcManhourTrendWin()
        self.nrc_trend_win.show()

    @pyqtSlot()
    def on_toolButtonRtnQuotationAssistant_clicked(self):  # TODO
        pass

    @pyqtSlot()
    def on_toolButtonRtnMhTrend_clicked(self):  # TODO
        pass

    @pyqtSlot()
    def on_pushButtonSearch_clicked(self):
        # self.table_name = "MhFinalized"
        has_nrc = self.ui.checkBoxNrc.isChecked()
        has_rtn = self.ui.checkBoxRtn.isChecked()
        filter_str = None
        if self.ui.radioButtonBySimi.isChecked():
            desc = self.ui.lineEditSearchDesc.text()
            corpus = ManhourVectorCorpus()
            sims = self.ui.doubleSpinBoxSims.value()
            results = corpus.get_similarity_by_latest(search_text=desc, threshold=sims)

            # 获得的结果是数据库记录的位置，而非mh_id，所以还要查询数据库以获得mh_id具体内容
            self.query.prepare(f"SELECT mh_id,description FROM {self.table_name} LIMIT 1 OFFSET :offset")
            coll_id = []
            for r in results:
                self.query.bindValue(":offset", r[0])
                if self.query.exec() and self.query.first():
                    coll_id.append(self.query.value('mh_id'))
            if coll_id:
                filter_str = ' OR '.join([f"mh_id='{x}'" for x in coll_id])
            else:
                filter_str = 'mh_id=-1'

        if self.ui.radioButtonByWord.isChecked():
            condition = {}
            if self.ui.lineEditSearchId.text():
                condition['mh_id'] = self.ui.lineEditSearchId.text()
            if self.ui.lineEditSearchAcType.text():
                condition['ac_type'] = self.ui.lineEditSearchAcType.text()
            if self.ui.lineEditSearchRegister.text():
                condition['register'] = self.ui.lineEditSearchRegister.text()
            if self.ui.lineEditSearchPkgId.text():
                condition['pkg_id'] = self.ui.lineEditSearchPkgId.text()
            if self.ui.lineEditSearchDesc.text():
                condition['description'] = self.ui.lineEditSearchDesc.text()
            filter_str = ' AND '.join([f"{field} LIKE '%{value}%'" for field, value in condition.items()])

        if filter_str:
            if has_nrc and not has_rtn:
                filter_str += " AND class='NRC'"
            elif not has_nrc and has_rtn:
                filter_str += " AND class='RTN'"
            elif not has_nrc and not has_rtn:
                filter_str += " AND class!='NRC' AND class!='RTN'"
            else:
                pass
        else:
            if has_nrc and not has_rtn:
                filter_str = "class='NRC'"
            elif not has_nrc and has_rtn:
                filter_str = "class='RTN'"
            elif not has_nrc and not has_rtn:
                filter_str = "class!='NRC' AND class!='RTN'"
            else:
                filter_str = "class='NRC' OR class='RTN'"
        self.table_model.setFilter(filter_str)
        self.table_model.select()

    @pyqtSlot()
    def on_pushButtonImport_clicked(self):
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
        converters = {'WO': lambda y: str(y),
                      'Description': lambda y: str(y).strip(),
                      'ATA': lambda y: str(y),
                      'Zone': lambda y: str(y),
                      'Skill': lambda y: f'{y:.2f}',
                      'Unskill': lambda y: f'{y:.2f}',
                      'Total': lambda y: f'{y:.2f}',
                      'D_Skill': lambda y: f'{y:.2f}',
                      'D_Unskill': lambda y: f'{y:.2f}',
                      'D_Total': lambda y: f'{y:.2f}', }
        df = pd.read_excel(read_path, keep_default_na=False, converters=converters)
        query = QtSql.QSqlQuery(self.db.con)
        query.prepare(f"""REPLACE INTO {self.table_name}
                          VALUES ({','.join(['?' for _ in range(self.table_model.columnCount())])})""")
        self.db.con.transaction()
        for i in range(df.shape[0]):
            for field, column in self.field_num.items():
                header = TABLE_HEADER_MAPPING[field]
                query.addBindValue(df.loc[i, header])
            if not query.exec_():
                self.db.con.rollback()
                QtWidgets.QMessageBox.critical(self, 'Error', f'Failed\n{self.query.lastError().text()}')
                return

        self.db.con.commit()
        QtWidgets.QMessageBox.information(self, 'Information', 'Import successfully!')

    @pyqtSlot()
    def on_pushButtonExport_clicked(self):
        today = QDateTime.currentDateTime().toString('yyyy_MM_dd_hh_mm_ss')
        filename = f'MH_NRC_Finalized_{today}.xlsx'
        save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", filename, "Excel Files (*.xlsx)")
        if not save_path:
            return

        save_path = Path(save_path).resolve()
        # 创建工时记录DataFrame对象
        data = []
        header = []
        for j in range(self.table_model.columnCount()):
            header.append(self.table_model.headerData(j, Qt.Horizontal, Qt.DisplayRole))

        for i in range(self.table_model.rowCount()):
            row_data = []
            for j in range(self.table_model.columnCount()):
                row_data.append(self.table_model.data(self.table_model.index(i, j), Qt.DisplayRole))
            data.append(row_data)
        df = pd.DataFrame(data, columns=header)
        df.to_excel(save_path, index=False)
        # 打开保存文件夹
        os.startfile(save_path.cwd())

    @pyqtSlot()
    def on_pushButtonDelete_clicked(self):
        selected_indexes = self.selection_model.selectedRows(column=self.field_num['mh_id'])
        if not selected_indexes:
            QtWidgets.QMessageBox.information(self, 'Information', 'No row(s) selected!')
            return
        choose = QtWidgets.QMessageBox.warning(self, 'Warning', 'Are you sure to delete?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choose == QtWidgets.QMessageBox.Yes:
            self.query.prepare(f"DELETE FROM {self.table_name} WHERE mh_id=:mh_id")
            self.db.con.transaction()
            for index in selected_indexes:
                self.query.bindValue(':mh_id', index.data())
                self.query.exec()
            if self.db.con.commit():
                QtWidgets.QMessageBox.information(self, 'Information', 'Deleted!')
                self.table_model.select()
            else:
                QtWidgets.QMessageBox.critical(self, 'Error', self.db.con.lastError().text())

    @pyqtSlot()
    def on_pushButtonDetail_clicked(self):
        sel_model = self.ui.tableView.selectionModel()
        if len(sel_model.selectedRows(self.field_num['mh_id'])) != 1:
            QtWidgets.QMessageBox.information(self, 'Information', 'One row should be selected!')
            return
        fields = list(TABLE_HEADER_MAPPING.keys())
        data = {fields[i]: idx.data(Qt.DisplayRole) for i, idx in enumerate(sel_model.selectedIndexes())}
        self.detail_win = ManhourFinalizedWin()
        self.detail_win.setData(**data)
        self.detail_win.show()

    @pyqtSlot()
    def on_pushButtonSubtask_clicked(self):
        sel_model = self.ui.tableView.selectionModel()
        selected_rowIndexes = sel_model.selectedRows(column=self.field_num['mh_id'])
        if len(selected_rowIndexes) != 1:
            QtWidgets.QMessageBox.information(self, 'Information', 'One row should be selected!')
            return
        mh_id = selected_rowIndexes[0].data()
        self.subtask_win = NrcSubtaskTempWin(mh_id)
        self.subtask_win.show()

    @pyqtSlot()
    def on_pushButtonAddImage_clicked(self):
        sel_model = self.ui.tableView.selectionModel()
        sel_rowIndexes = sel_model.selectedRows(column=self.field_num['mh_id'])
        if not sel_rowIndexes:
            QtWidgets.QMessageBox.information(self, 'Information', 'No row(s) selected!')
            return

        file_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Open Image", "",
                                                               "Image Files (*.png *.jpg *.bmp)")
        if not file_paths:
            return
        sql = """INSERT INTO MhImage
                         VALUES (:id,:mh_id,:name,:image,(SELECT IFNULL(MAX(sheet)+1,1) FROM MhImage WHERE mh_id=:mh_id))"""
        self.db.con.transaction()  # 创建事务
        self.query.prepare(sql)
        for file_path in file_paths:
            with open(file_path, 'rb') as f:
                image_data = QtCore.QByteArray(f.read())  # 以二进制模式打开图片数据并转化为QByteArray对象
            path = Path(file_path)
            for index in sel_rowIndexes:
                self.query.bindValue(':id', None)
                self.query.bindValue(':mh_id', index.data())
                self.query.bindValue(':name', path.name)
                self.query.bindValue(':image', image_data)
                if not self.query.exec():
                    self.db.con.rollback()
                    QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
                    return
        self.db.con.commit()
        QtWidgets.QMessageBox.information(self, 'Information', 'Successfully')

    @pyqtSlot()
    def on_pushButtonImage_clicked(self):
        sel_model = self.ui.tableView.selectionModel()
        sel_rowIndexes = sel_model.selectedRows(column=self.field_num['mh_id'])
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

    def on_radioButtonBySimi_toggled(self, checked):
        if checked:
            self.ui.doubleSpinBoxSims.setEnabled(True)
            self.ui.lineEditSearchId.setEnabled(False)
            self.ui.lineEditSearchAcType.setEnabled(False)
            self.ui.lineEditSearchRegister.setEnabled(False)
            self.ui.lineEditSearchPkgId.setEnabled(False)
        else:
            self.ui.doubleSpinBoxSims.setEnabled(False)
            self.ui.lineEditSearchId.setEnabled(True)
            self.ui.lineEditSearchAcType.setEnabled(True)
            self.ui.lineEditSearchRegister.setEnabled(True)
            self.ui.lineEditSearchPkgId.setEnabled(False)
            self.ui.doubleSpinBoxSims.setValue(0.9)

    def show_table_header_menu(self, pos):
        # 创建右键菜单
        menu = QtWidgets.QMenu(self)
        # 获取右键点击处的列索引
        column = self.ui.tableView.horizontalHeader().logicalIndexAt(pos)
        # 添加菜单项
        if self.ui.tableView.horizontalHeader().sectionResizeMode(column) == QtWidgets.QHeaderView.Interactive:
            column_resizable_action = QtWidgets.QAction("Non-resizable", self)
        else:
            column_resizable_action = QtWidgets.QAction("Resizable", self)
        column_resizable_action.triggered.connect(lambda: self.set_column_resizable(pos))
        menu.addAction(column_resizable_action)

        # 显示右键菜单
        menu.exec_(self.ui.tableView.viewport().mapToGlobal(pos))

    def set_column_resizable(self, pos):
        # 获取右键点击处的列索引
        column = self.ui.tableView.horizontalHeader().logicalIndexAt(pos)

        if self.ui.tableView.horizontalHeader().sectionResizeMode(column) == QtWidgets.QHeaderView.Interactive:
            self.ui.tableView.horizontalHeader().setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)
        else:
            self.ui.tableView.horizontalHeader().setSectionResizeMode(column, QtWidgets.QHeaderView.Interactive)
