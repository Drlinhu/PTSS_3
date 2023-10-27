import os
from pathlib import Path

import pandas as pd
from PyQt5 import QtWidgets, QtSql, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot, QDate, Qt, QDateTime
from PyQt5.QtGui import QStandardItem

from ..ui import Ui_RegisterProjectIdForm
from ..ui import Ui_NewRegProjInputDialog
from .nrc_register_dashborad import RegisterNrcDailyWin
from utils.database import DatabaseManager


class NrcManhourTrendWin(QtWidgets.QWidget):
    proj_h_header_label = {'register': 'Register',
                           'proj_id': 'Project ID',
                           'start_date': 'Start Date',
                           'end_date': 'End Date',
                           'duration': 'Duration',
                           'status': 'Status'}
    trend_h_header_label = ['Register', 'Project_ID', 'Report_Date', 'Total']

    def __init__(self, parent=None):
        super().__init__(parent)
        self.table_reg_proj = "RegisterProjectId"
        self.db = DatabaseManager()
        self.query = QtSql.QSqlQuery(self.db.con)
        self.ui = Ui_RegisterProjectIdForm()
        self.ui.setupUi(self)
        self.setFixedSize(1000, 600)
        self.ui.dateEditSearchStart.setDate(QDate.currentDate().addMonths(-3))
        self.ui.dateEditSearchEnd.setDate(QDate.currentDate().addYears(1))

        self.init_projectId_table()
        self.init_manhour_trend_table()

    def on_tbvRegisterProjId_clicked(self, index: QtCore.QModelIndex):
        reg = self.ui.tbvRegisterProjId.model().index(index.row(), self.proj_field_num['register']).data()
        proj_id = self.ui.tbvRegisterProjId.model().index(index.row(), self.proj_field_num['proj_id']).data()
        self.ui.lineEditRegister.setText(reg)
        self.ui.lineEditProjectId.setText(proj_id)

        sql = f"""SELECT register,SUBSTR(nrc_id,1,2),report_date,sum(total) 
                  FROM MhNrcReport 
                  WHERE register=:reg AND SUBSTR(nrc_id,1,2)=:proj_id
                  GROUP BY report_date
                  ORDER BY report_date ASC"""
        self.query.prepare(sql)
        self.query.bindValue(':reg', reg)
        self.query.bindValue(':proj_id', proj_id)
        self.query.exec()

        model: QtGui.QStandardItemModel = self.ui.tbvMhDailyTotal.model()
        model.removeRows(0, model.rowCount())

        while self.query.next():
            temp = []
            for i in range(model.columnCount()):
                item = self.query.value(i)
                if isinstance(item, (float, int)):
                    item = f"{item:.2f}"
                temp.append(QStandardItem(item))
            model.appendRow(temp)

        # 设置当前最新记录的total
        cur_total = model.index(model.rowCount() - 1, 3).data()
        self.ui.lineEditTotal.setText(cur_total)

    def on_tbvRegisterProjId_doubleClicked(self, index: QtCore.QModelIndex):
        reg = self.ui.tbvRegisterProjId.model().index(index.row(), self.proj_field_num['register']).data()
        proj_id = self.ui.tbvRegisterProjId.model().index(index.row(), self.proj_field_num['proj_id']).data()
        start_date = self.ui.tbvRegisterProjId.model().index(index.row(), self.proj_field_num['start_date']).data()
        end_date = self.ui.tbvRegisterProjId.model().index(index.row(), self.proj_field_num['end_date']).data()
        status = self.ui.tbvRegisterProjId.model().index(index.row(), self.proj_field_num['status']).data()
        dialog = RegisterProjInputDialog()
        dialog.ui.ccbRegister.setCurrentText(reg)
        dialog.ui.lineEditProj.setText(proj_id)
        dialog.ui.dateEditStart.setDate(QDate(*[int(x)for x in start_date.split('-')]))
        dialog.ui.dateEditEnd.setDate(QDate(*[int(x)for x in end_date.split('-')]))
        dialog.ui.ccbStaus.setCurrentText(status)
        dialog.exec()

    def on_tbvMhDailyTotal_doubleClicked(self, index: QtCore.QModelIndex):
        register = self.ui.tbvMhDailyTotal.model().index(index.row(), 0).data()
        proj_id = self.ui.tbvMhDailyTotal.model().index(index.row(), 1).data()
        report_date = self.ui.tbvMhDailyTotal.model().index(index.row(), 2).data()
        self.daily_win = RegisterNrcDailyWin(report_date, register, proj_id)
        self.daily_win.show()

    @pyqtSlot()
    def on_btnSearch_clicked(self):
        data_model: QtSql.QSqlTableModel = self.ui.tbvRegisterProjId.model()
        condition = {}
        if self.ui.lineEditSearchRegister.text():
            condition['register'] = self.ui.lineEditSearchRegister.text()
        if self.ui.ccbSearchProjectId.currentText():
            condition['proj_id'] = self.ui.ccbSearchProjectId.currentText()
        if self.ui.ccbSearchStaus.currentText():
            condition['status'] = self.ui.ccbSearchStaus.currentText()
        dt_start = self.ui.dateEditSearchStart.date().toString('yyyy-MM-dd')
        dt_end = self.ui.dateEditSearchEnd.date().toString('yyyy-MM-dd')
        filter_str_1 = f"start_date>='{dt_start}' AND end_date<='{dt_end}'"
        if condition:
            filter_str_2 = " AND ".join([f"{f} LIKE '%{v}%'" for f, v in condition.items()])
            data_model.setFilter(filter_str_1 + ' AND ' + filter_str_2 + 'ORDER BY start_date DESC')
        else:
            data_model.setFilter(filter_str_1 + 'ORDER BY start_date DESC')
        data_model.select()

    @pyqtSlot()
    def on_btnNew_clicked(self):
        dialog = RegisterProjInputDialog()
        dialog.exec()
        self.on_btnSearch_clicked()

    @pyqtSlot()
    def on_btnDelete_clicked(self):
        data_model = self.ui.tbvRegisterProjId.model()
        sel_model = self.ui.tbvRegisterProjId.selectionModel()
        sel_indexes = sel_model.selectedRows(column=self.proj_field_num['register'])
        if not sel_indexes:
            QtWidgets.QMessageBox.information(self, 'Information', 'No row(s) selected!')
            return
        choose = QtWidgets.QMessageBox.warning(self, 'Warning', 'Are you sure to delete?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choose == QtWidgets.QMessageBox.Yes:
            self.db.con.transaction()
            self.query.prepare(f"""DELETE FROM {self.table_reg_proj} WHERE register=:reg AND proj_id=:proj_id""")
            for idx in sel_indexes:
                reg = data_model.index(idx.row(), self.proj_field_num['register']).data()
                proj_id = data_model.index(idx.row(), self.proj_field_num['proj_id']).data()
                self.query.bindValue(':reg', reg)
                self.query.bindValue(':proj_id', proj_id)
                if not self.query.exec():
                    self.db.con.rollback()
                    QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text(), )
                    return
            self.db.con.commit()
            QtWidgets.QMessageBox.information(self, 'Information', 'Deleted!')
            self.on_btnSearch_clicked()

    @pyqtSlot()
    def on_btnExport_clicked(self):
        today = QDateTime.currentDateTime().toString('yyyy_MM_dd_hh_mm_ss')
        filename = f'MH_NRC_Trend_{today}.xlsx'
        save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", filename, "Excel Files (*.xlsx *.xls)")
        if not save_path:
            return

        save_path = Path(save_path).resolve()

        # 创建NRC工时DataFrame对象
        model = self.ui.tbvMhDailyTotal.model()
        data = []
        for i in range(model.rowCount()):
            row_data = []
            for j in range(model.columnCount()):
                if self.trend_h_header_label[j] == 'Total':
                    row_data.append(float(model.index(i, j).data()))
                else:
                    row_data.append(model.index(i, j).data())

            data.append(row_data)
        df = pd.DataFrame(data, columns=self.trend_h_header_label)
        df.to_excel(save_path, index=False)
        # 打开保存文件夹
        os.startfile(save_path.parent)

    @pyqtSlot()
    def on_btnChart_clicked(self):  # TODO
        pass

    def init_projectId_table(self):
        h_header = self.ui.tbvRegisterProjId.horizontalHeader()
        # 创建表格模型(可编辑, 默认可排序)
        data_model = QtSql.QSqlTableModel(self, self.db.con)
        data_model.setTable(self.table_reg_proj)
        # 创建选择模型
        sel_model = QtCore.QItemSelectionModel(data_model)
        # 设置表格数据模型和选择模型
        self.ui.tbvRegisterProjId.setModel(data_model)
        self.ui.tbvRegisterProjId.setSelectionModel(sel_model)
        # 设置表格标题
        self.proj_field_num = self.db.get_field_num(data_model)
        for field, column in self.proj_field_num.items():  # 设置字段显示名
            data_model.setHeaderData(column, Qt.Horizontal, self.proj_h_header_label[field])
        h_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        # 设置表格视图内容右击弹出菜单
        self.ui.tbvRegisterProjId.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tbvRegisterProjId.customContextMenuRequested.connect(self.show_proj_table_menu)

        self.on_btnSearch_clicked()

    def init_manhour_trend_table(self):
        h_header = self.ui.tbvMhDailyTotal.horizontalHeader()
        # 创建表格模型(可编辑, 默认可排序)
        data_model = QtGui.QStandardItemModel()
        data_model.setHorizontalHeaderLabels(self.trend_h_header_label)

        # 设置表格数据模型和选择模型
        self.ui.tbvMhDailyTotal.setModel(data_model)
        # 设置表格标题
        h_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        h_header.setStretchLastSection(True)

    def show_proj_table_menu(self, pos):
        # 创建右键菜单
        menu = QtWidgets.QMenu(self)
        # 获取右键点击处的列索引
        index = self.ui.tbvRegisterProjId.indexAt(pos)
        action_close = QtWidgets.QAction("Close", self)
        action_close.triggered.connect(lambda: self.set_project_status_closed(index))
        menu.addAction(action_close)
        # 显示右键菜单
        menu.exec_(self.ui.tbvRegisterProjId.viewport().mapToGlobal(pos))

    def set_project_status_closed(self, index):
        data_model = self.ui.tbvRegisterProjId.model()
        row = index.row()
        reg = data_model.index(row, self.proj_field_num['register']).data()
        proj_id = data_model.index(row, self.proj_field_num['proj_id']).data()
        sql = f"""UPDATE {self.table_reg_proj}
                  SET status='CLOSED'
                  WHERE register=:reg AND proj_id=:proj_id"""
        self.query.prepare(sql)
        self.query.bindValue(':reg', reg)
        self.query.bindValue(':proj_id', proj_id)
        self.query.exec()
        self.on_btnSearch_clicked()


class RegisterProjInputDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table_reg_proj = "RegisterProjectId"
        self.db = DatabaseManager()
        self.query = QtSql.QSqlQuery(self.db.con)

        self.ui = Ui_NewRegProjInputDialog()
        self.ui.setupUi(self)
        self.ui.dateEditStart.setDate(QDate.currentDate())
        self.ui.dateEditEnd.setDate(QDate.currentDate())

    @pyqtSlot()
    def on_btnSave_clicked(self):
        reg = self.ui.ccbRegister.currentText()
        proj_id = self.ui.lineEditProj.text()
        dt_start = self.ui.dateEditStart.date().toString('yyyy-MM-dd')
        dt_end = self.ui.dateEditEnd.date().toString('yyyy-MM-dd')
        duration = self.ui.dateEditStart.date().daysTo(self.ui.dateEditEnd.date())
        status = self.ui.ccbStaus.currentText()
        if reg == "" or proj_id == "":
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Please fill in all fields.')
        else:
            sql = f"""REPLACE INTO {self.table_reg_proj} VALUES (:reg,:proj_id,:dt_start,:dt_end,:duration,:status)"""
            self.query.prepare(sql)
            self.query.bindValue(':reg', reg)
            self.query.bindValue(':proj_id', proj_id)
            self.query.bindValue(':dt_start', dt_start)
            self.query.bindValue(':dt_end', dt_end)
            self.query.bindValue(':duration', str(duration))
            self.query.bindValue(':status', status)
            if not self.query.exec():
                QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
            else:
                QtWidgets.QMessageBox.information(self, 'Information', 'Saved.')
                self.close()

    @pyqtSlot()
    def on_btnCancel_clicked(self):
        self.close()
