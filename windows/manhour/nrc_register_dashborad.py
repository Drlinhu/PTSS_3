import os
from pathlib import Path
import pandas as pd
from PyQt5 import QtWidgets, QtSql, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSlot, QDate

from ..ui import Ui_RegisterNrcDailyDetailForm
from windows.image_viewer import ImageViewer
from utils.database import DatabaseManager


class RegisterNrcDailyWin(QtWidgets.QWidget):
    tb_header_summary = {"Horizontal": ["AE", "AI", "AV", "CL", "GW", "PT", "SM", "SS", "TOTAL", "CHANGED"],
                         "Vertical": ["CAB", "EMP", "ENG", "F/T", "FUS", "LDG", "LWR", "WNG", "TOTAL", "CHANGED"], }
    tb_header_nrc = ["Nrc_Id", "Ref_Task", "Description", "Area", "Status", "Total", "Added_On", "Changed"]
    tb_header_history = ['Register', 'Project_ID', 'Report_Date', 'Total']

    def __init__(self, report_date, register, proj_id, parent=None):
        super(RegisterNrcDailyWin, self).__init__(parent)
        self.report_date = report_date
        self.register = register
        self.proj_id = proj_id
        self.total_qty = 0
        self.total_mhr = 0

        self.db = DatabaseManager()
        self.query = QtSql.QSqlQuery(self.db.con)

        self.tb_name_nrc = "MhNrcReport"
        self.tb_name_finalized = "MhFinalized"

        self.ui = Ui_RegisterNrcDailyDetailForm()
        self.ui.setupUi(self)
        # self.showMaximized()

        self.ui.lineEditRegister.setText(register)
        self.ui.dateEdit.setDate(QDate(*[int(x) for x in report_date.split('-')]))

        # 初始化added_on控件选项
        sql = f"""SELECT report_date
                  FROM {self.tb_name_nrc}
                  WHERE register=:reg AND SUBSTR(nrc_id,1,2)=:proj_id
                  GROUP BY report_date
                  ORDER BY report_date ASC"""
        self.query.prepare(sql)
        self.query.bindValue(':reg', register)
        self.query.bindValue(':proj_id', proj_id)
        self.query.exec()
        self.added_date = []
        while self.query.next():
            self.added_date.append(self.query.value(0))
        self.ui.cbbSearchAddedOn.addItems([''] + self.added_date)

        self.tableviews = {'AE': self.ui.tbvAE,
                           'AI': self.ui.tbvAI,
                           'AV': self.ui.tbvAV,
                           'CL': self.ui.tbvCL,
                           'GW': self.ui.tbvGW,
                           'PT': self.ui.tbvPT,
                           'SM': self.ui.tbvSM,
                           'SS': self.ui.tbvSS}
        self.trade_fields = ['nrc_id', 'ref_task', 'description', 'area', 'status', 'total', 'added_on', 'changed']

        # 初始化表格
        self.init_table_summary()
        self.init_table_nrc()

    @pyqtSlot()
    def on_btnSearch_clicked(self):
        self.ui.checkBoxChanged.setChecked(False)
        cur_idx = self.ui.tabWidgetNrcByTR.currentIndex()
        tr, table = list(self.tableviews.items())[cur_idx]

        condition = {}
        if self.ui.lineEditSearchNrcId.text():
            condition['nrc_id'] = self.ui.lineEditSearchNrcId.text()
        if self.ui.lineEditSearchRefTask.text():
            condition['ref_task'] = self.ui.lineEditSearchRefTask.text()
        if self.ui.lineEditSearchDesc.text():
            condition['description'] = self.ui.lineEditSearchDesc.text()
        if self.ui.cbbSearchArea.currentText():
            condition['area'] = self.ui.cbbSearchArea.currentText()

        if condition:
            filter_str = ' AND '.join([f"{field} LIKE '%{value}%'" for field, value in condition.items()])
            self.update_table_nrc(tr, table, filter_str)
        else:
            self.update_table_nrc(tr, table)

    def on_checkBoxChanged_stateChanged(self, state):
        # 2搭扣
        for table in self.tableviews.values():
            model: QtGui.QStandardItemModel = table.model()
            if state == 0:
                for row in range(model.rowCount()):
                    table.showRow(row)
            elif state == 2:
                for row in range(model.rowCount()):
                    changed_mhr = float(model.item(row, self.trade_fields.index('changed')).text())
                    if changed_mhr == 0:
                        table.hideRow(row)

    @pyqtSlot(str)
    def on_cbbSearchAddedOn_activated(self, date):
        cur_idx = self.ui.tabWidgetNrcByTR.currentIndex()
        table = list(self.tableviews.values())[cur_idx]
        model: QtGui.QStandardItemModel = table.model()
        for row in range(model.rowCount()):
            item = model.item(row, self.trade_fields.index('added_on'))
            if date == "":
                self.ui.checkBoxChanged.setChecked(False)
                table.showRow(row)
            elif item.text() != date:
                table.hideRow(row)
            else:
                table.showRow(row)

    def init_table_summary(self):
        tableviews = [self.ui.tbvMhr, self.ui.tbvMhrChanged]
        for table in tableviews:
            model = QtGui.QStandardItemModel()
            model.setColumnCount(len(self.tb_header_summary["Horizontal"]))
            model.setRowCount(len(self.tb_header_summary["Vertical"]))
            model.setHorizontalHeaderLabels(self.tb_header_summary["Horizontal"])
            model.setVerticalHeaderLabels(self.tb_header_summary["Vertical"])
            table.setModel(model)
            # 设置表格标题
            h_header = table.horizontalHeader()
            h_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
            h_header.setStretchLastSection(True)

    def update_table_summary_data(self):
        pass
        # # 设置单元格背景颜色
        # for row in range(self.model.rowCount()):
        #     value = int(self.model.item(row, 1).text())
        #     if value > 15:
        #         color = QtGui.QColor(255, 0, 0)  # 红色
        #     else:
        #         color = QtGui.QColor(0, 255, 0)  # 绿色
        #     brush = QtGui.QBrush(color)
        #     self.model.item(row, 1).setBackground(brush)

    def init_table_nrc(self):
        """初始化表格及数据"""
        for tr, table in self.tableviews.items():
            model = QtGui.QStandardItemModel()
            model.setHorizontalHeaderLabels(self.tb_header_nrc)
            table.setModel(model)

            # 设置表格标题
            h_header = table.horizontalHeader()
            h_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
            h_header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

            self.update_table_nrc(tr, table)

    def update_table_nrc(self, tr, table: QtWidgets.QTableView, filter_str=None):
        model = table.model()
        model.removeRows(0, model.rowCount())
        if filter_str:
            sql = f"""SELECT nrc_id,ref_task,description,area,status,total,
                             min(report_date) as added_on,max(report_date) as latest_date
                      FROM MhNrcReport
                      WHERE register=:register AND SUBSTR(nrc_id,1,2)=:proj_id AND trade=:trade AND {filter_str}
                      GROUP BY nrc_id
                      ORDER BY nrc_id ASC"""
        else:
            sql = f"""SELECT nrc_id,ref_task,description,area,status,total,
                             min(report_date) as added_on,max(report_date) as latest_date
                      FROM MhNrcReport
                      WHERE register=:register AND SUBSTR(nrc_id,1,2)=:proj_id AND trade=:trade
                      GROUP BY nrc_id
                      ORDER BY nrc_id ASC"""
        # 获取最新日期的报告
        self.query.prepare(sql)
        self.query.bindValue(":register", self.register)
        self.query.bindValue(":proj_id", self.proj_id)
        self.query.bindValue(":trade", tr)
        self.query.exec()
        while self.query.next():
            temp = []
            for field in self.trade_fields:
                if field == 'total':
                    item = QtGui.QStandardItem(f"{self.query.value(field):.2f}")
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                elif field == 'changed':
                    item = QtGui.QStandardItem("0.00")
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                else:
                    item = QtGui.QStandardItem(self.query.value(field))
                temp.append(item)
            model.appendRow(temp)

        """计算changed值"""
        sql = f"""SELECT total 
                  FROM {self.tb_name_nrc} 
                  WHERE nrc_id=:nrc_id 
                  ORDER BY report_date DESC 
                  LIMIT 2"""
        self.query.prepare(sql)
        for row in range(model.rowCount()):
            nrc_id = model.index(row, self.trade_fields.index('nrc_id')).data()
            self.query.bindValue(":nrc_id", nrc_id)
            self.query.exec()
            r = []
            while self.query.next():
                r.append(self.query.value('total'))
            if len(r) == 1:  # 说明数据是新增的
                color = QtGui.QColor(240, 230, 140)  # 黄褐色
                brush = QtGui.QBrush(color)
                for col in range(model.columnCount()):
                    item = model.item(row, col)
                    item.setBackground(brush)
                    if self.trade_fields[col] == 'changed':
                        item.setText(f"{r[0]:.2f}")
            else:
                item = model.item(row, self.trade_fields.index('changed'))
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                item.setText(f"{r[0] - r[1]:.2f}")

        self.render_table_nrc(table)

    def render_table_nrc(self, table: QtWidgets.QTableView):
        model: QtGui.QStandardItemModel = table.model()
        for row in range(model.rowCount()):
            item = model.item(row, self.trade_fields.index('changed'))
            if float(item.text()) > 0:  # 工时增加了
                color = QtGui.QColor(250, 128, 114)  # 红色
            elif float(item.text()) < 0:
                color = QtGui.QColor(0, 250, 154)  # 红色
            else:
                color = QtGui.QColor(255, 255, 255)  # 白色
            brush = QtGui.QBrush(color)
            item.setBackground(brush)
