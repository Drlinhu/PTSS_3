import os
from xlsxwriter.workbook import Workbook, Worksheet
from pathlib import Path
import pandas as pd
from PyQt5 import QtWidgets, QtSql, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSlot, QDate, QDateTime

from ..ui import Ui_RegisterNrcDailyDetailForm, Ui_NrcReportDetailForm
from .mh_finalized_detail_win import ManhourFinalizedWin
from .nrc_subtask_temp_win import NrcSubtaskTempWin
from .cx_remark_dialog import CxRemarkInputDialog
from windows.image_viewer import ImageViewer
from utils.database import DatabaseManager
from utils.nrc_corpus import *


class RegisterNrcDailyWin(QtWidgets.QWidget):
    tb_header_summary = {"Horizontal": ["AE", "AI", "AV", "CL", "GW", "PT", "SM", "SS", "TOTAL", ],
                         "Vertical": ["CAB", "EMP", "ENG", "F/T", "FUS", "LDG", "LWR", "WNG", "TOTAL", ], }
    tb_header_nrc = ["Nrc_Id", "Ref_Task", "Description", "Area", "Status", "Total", "Added_On", "Changed", "Remark"]
    tb_header_history = ['MH_ID', 'Register', 'Description', 'Total', 'Simis']

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
        self.showMaximized()

        self.ui.lineEditRegister.setText(register)
        self.ui.dateEdit.setDate(QDate(*[int(x) for x in report_date.split('-')]))

        # 初始化added_on控件选项
        sql = f"""SELECT report_date
                  FROM {self.tb_name_nrc}
                  WHERE register=:reg AND SUBSTR(nrc_id,1,2)=:proj_id AND report_date<=:report_date
                  GROUP BY report_date
                  ORDER BY report_date ASC"""
        self.query.prepare(sql)
        self.query.bindValue(':reg', register)
        self.query.bindValue(':proj_id', proj_id)
        self.query.bindValue(':report_date', self.report_date)
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
        self.trade_fields = ['nrc_id', 'ref_task', 'description', 'area', 'status', 'total', 'added_on', 'changed',
                             'remark']

        # 初始化表格
        self.init_table_summary()
        self.init_table_nrc()
        self.init_history_table()

        # 设置界面信息
        total_qty_tr = 0
        total_mhr_tr = 0
        for tr, table in self.tableviews.items():
            model = table.model()
            total_qty_tr += model.rowCount()
            for row in range(model.rowCount()):
                total_mhr_tr += float(model.index(row, self.trade_fields.index('total')).data())
        self.ui.lineEditTotalQtyTR.setText(f"{total_qty_tr:.2f}")
        self.ui.lineEditTotalMhrTR.setText(f"{total_mhr_tr:.2f}")

        sql = f"""SELECT COUNT(*) AS qty,sum(total) AS total
                  FROM {self.tb_name_nrc}
                  WHERE register=:reg AND SUBSTR(nrc_id,1,2)=:proj_id AND report_date=:report_date"""
        self.query.prepare(sql)
        self.query.bindValue(':reg', register)
        self.query.bindValue(':proj_id', proj_id)
        self.query.bindValue(':report_date', self.report_date)
        self.query.exec()
        if self.query.first():
            self.ui.lineEditTotalQtyReportS.setText(f"{self.query.value('qty'):.2f}")
            self.ui.lineEditTotalMhrReport.setText(f"{self.query.value('total'):.2f}")

        # 设置槽函数
        self.ui.lineEditSearchNrcId.returnPressed.connect(self.on_btnSearch_clicked)
        self.ui.lineEditSearchRefTask.returnPressed.connect(self.on_btnSearch_clicked)
        self.ui.lineEditSearchDesc.returnPressed.connect(self.on_btnSearch_clicked)
        self.ui.tbvHistory.doubleClicked.connect(lambda idx: self.on_btnHistoryDetail_clicked())

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

    @pyqtSlot()
    def on_btnExport_clicked(self):
        today = QDateTime.currentDateTime().toString('yyyy_MM_dd')
        filename = f'MH_NRC_REPORT_{today}.xlsx'
        save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", filename,
                                                             "Excel Files (*.xlsx *.xls)")
        if not save_path:
            return
        save_path = Path(save_path).resolve()
        output_tr = []
        # 创建Excel Writer对象
        writer = pd.ExcelWriter(save_path)
        workbook: Workbook = writer.book

        # 读取导出模式
        options = QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel
        choose = QtWidgets.QMessageBox.information(self, 'Information', 'Are you want to export all page?', options)
        if choose == QtWidgets.QMessageBox.Cancel:
            return
        elif choose == QtWidgets.QMessageBox.Yes:  # 导出全部页
            output_tr = list(self.tableviews.keys())
        else:
            output_tr.append(list(self.tableviews.keys())[self.ui.tabWidgetNrcByTR.currentIndex()])

        df_dict = {'Total': pd.DataFrame(columns=self.tb_header_nrc + ['Trade']),
                   'Duplicated': pd.DataFrame(columns=self.tb_header_nrc + ['Trade']), }
        for tr in output_tr:
            table: QtWidgets.QTableView = self.tableviews[tr]
            model: QtGui.QStandardItemModel = table.model()
            data = []
            for row in range(model.rowCount()):
                if table.isRowHidden(row):
                    continue
                temp = []
                for col in range(model.columnCount()):
                    item = model.item(row, col)
                    if col in [5, 7]:
                        v = float(item.text())
                    else:
                        v = item.text()
                    temp.append(v)
                data.append(temp)
            df = pd.DataFrame(data=data, columns=self.tb_header_nrc)
            new_col = [tr] * df.shape[0]
            df_temp = df.assign(Trade=new_col)
            df_dict['Total'] = pd.concat([df_dict['Total'], df_temp], ignore_index=True)
            df_dict[tr] = df

        # 获取Nrc_Id重复行
        df_dict['Duplicated'] = df_dict['Total'][df_dict['Total'].duplicated(subset='Nrc_Id', keep=False)]

        # 写入并设置格式
        for sheet_name, df in df_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            # 获取Excel工作簿和工作表对象
            worksheet: Worksheet = writer.sheets[sheet_name]

            # 设置数值列的格式为小数两位
            _format = workbook.add_format({'num_format': '0.00'})
            for col in ['Total', 'Changed']:
                column_index = df.columns.get_loc(col)
                worksheet.set_column(column_index, column_index, 6, _format)

            # 设置日期列的格式为日期
            _format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
            column_index = df.columns.get_loc('Added_On')
            worksheet.set_column(column_index, column_index, 10, _format)

        # 保存Excel文件
        writer.close()

        # 打开保存文件夹
        os.startfile(save_path.parent)

    @pyqtSlot()
    def on_btnAddImage_clicked(self):
        table = list(self.tableviews.values())[self.ui.tabWidgetNrcByTR.currentIndex()]
        sel_model = table.selectionModel()
        sel_rowIdxes = sel_model.selectedRows(column=self.tb_header_nrc.index('Nrc_Id'))
        if not sel_rowIdxes:
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
            for index in sel_rowIdxes:
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
    def on_btnImage_clicked(self):
        table = list(self.tableviews.values())[self.ui.tabWidgetNrcByTR.currentIndex()]
        sel_model = table.selectionModel()
        sel_rowIdxes = sel_model.selectedRows(column=self.tb_header_nrc.index('Nrc_Id'))
        if len(sel_rowIdxes) != 1:
            QtWidgets.QMessageBox.information(self, 'Information', 'One row should be selected!')
            return
        ims = []
        mh_id = sel_rowIdxes[0].data()
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
    def on_btnDetail_clicked(self):
        table = list(self.tableviews.values())[self.ui.tabWidgetNrcByTR.currentIndex()]
        sel_model = table.selectionModel()
        sel_rowIdxes = sel_model.selectedRows(column=self.tb_header_nrc.index('Nrc_Id'))
        if len(sel_rowIdxes) != 1:
            QtWidgets.QMessageBox.information(self, 'Information', 'One row should be selected!')
            return
        nrc_id = sel_rowIdxes[0].data()
        self.report_detail = NrcReportDetailWin(self.register, nrc_id)
        self.report_detail.show()

    @pyqtSlot()
    def on_btnHistoryImage_clicked(self):
        sel_model: QtCore.QItemSelectionModel = self.ui.tbvHistory.selectionModel()
        sel_idxes = sel_model.selectedRows(column=0)  # nrc_id
        if len(sel_idxes) != 1:
            QtWidgets.QMessageBox.information(self, 'Information', 'One row should be selected!')
            return

        ims = []
        mh_id = sel_idxes[0].data()
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
        header_mapping = {'mh_id': 'MH_Id',
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
        sel_model: QtCore.QItemSelectionModel = self.ui.tbvHistory.selectionModel()
        sel_idxes = sel_model.selectedRows(column=0)  # nrc_id
        if len(sel_idxes) != 1:
            QtWidgets.QMessageBox.information(self, 'Information', 'One row should be selected!')
            return
        mh_id = sel_idxes[0].data()

        data = {}
        fields = list(header_mapping.keys())
        sql = "SELECT * FROM MhFinalized WHERE mh_id=:mh_id"
        self.query.prepare(sql)
        self.query.bindValue(":mh_id", mh_id)
        self.query.exec()
        if self.query.first():
            for field in fields:
                data[field] = self.query.value(field)

        self.detail_win = ManhourFinalizedWin()
        self.detail_win.setData(**data)
        self.detail_win.show()

    @pyqtSlot()
    def on_btnHistorySubtask_clicked(self):
        sel_model: QtCore.QItemSelectionModel = self.ui.tbvHistory.selectionModel()
        sel_idxes = sel_model.selectedRows(column=0)  # nrc_id
        if len(sel_idxes) != 1:
            QtWidgets.QMessageBox.information(self, 'Information', 'One row should be selected!')
            return
        nrc_id = sel_idxes[0].data()
        self.subtask_win = NrcSubtaskTempWin(nrc_id)
        self.subtask_win.show()

    def tbv_tr_double_clicked(self, index: QtCore.QModelIndex):
        # 历史表格初始化
        history_model: QtGui.QStandardItemModel = self.ui.tbvHistory.model()
        history_model.removeRows(0, history_model.rowCount())

        table: QtWidgets.QTableView = list(self.tableviews.values())[self.ui.tabWidgetNrcByTR.currentIndex()]
        model: QtGui.QStandardItemModel = table.model()
        row = index.row()
        desc = model.index(row, self.trade_fields.index('description')).data()
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
        for record in data:
            temp = []
            for value in record:
                item = QtGui.QStandardItem(str(value))
                temp.append(item)
            history_model.appendRow(temp)

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

        self.update_table_summary_data()

    def update_table_summary_data(self):
        def get_summary_data(date) -> pd.DataFrame:
            row_count = len(self.tb_header_summary["Vertical"])
            column_count = len(self.tb_header_summary["Horizontal"])
            df = pd.DataFrame(data=0.0, index=range(row_count), columns=range(column_count), )
            df.columns = self.tb_header_summary["Horizontal"]
            df.index = self.tb_header_summary["Vertical"]
            # 获取last report工时数据
            sql = f"""SELECT trade,area, sum(total) AS ttl
                      FROM {self.tb_name_nrc}
                      WHERE register=:register AND SUBSTR(nrc_id,1,2)=:proj_id AND report_date=:report_date
                      GROUP BY trade, area"""
            self.query.prepare(sql)
            self.query.bindValue(":register", self.register)
            self.query.bindValue(":proj_id", self.proj_id)
            self.query.bindValue(":report_date", date)
            self.query.exec()
            while self.query.next():
                tr = self.query.value('trade')
                area = self.query.value('area')
                df.loc[area, tr] = round(self.query.value('ttl'), 2)
            df['TOTAL'] = df.loc[:, 'AE':'SS'].sum(axis=1)
            df.loc['TOTAL'] = df.loc['CAB':'WNG', :].sum(axis=0)
            return df

        cur_date = self.report_date
        if len(self.added_date) > 1:
            idx = self.added_date.index(cur_date)
            last_date = self.added_date[idx if idx == 0 else idx - 1]
        else:
            last_date = cur_date
        df_last = get_summary_data(last_date)
        df_cur = get_summary_data(cur_date)
        df_diff = df_cur.sub(df_last).round(2)

        # 更新表数据
        model_mhr: QtGui.QStandardItemModel = self.ui.tbvMhr.model()
        model_chg: QtGui.QStandardItemModel = self.ui.tbvMhrChanged.model()
        for i in range(df_cur.shape[0]):
            for j in range(df_cur.shape[1]):
                item_mhr = QtGui.QStandardItem(f"{df_cur.iloc[i, j]:.2f}")
                item_chg = QtGui.QStandardItem(f"{df_diff.iloc[i, j]:.2f}")
                item_mhr.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                item_chg.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                if df_diff.iloc[i, j] > 0:
                    brush = QtGui.QBrush(QtGui.QColor(250, 128, 114))  # 红色
                elif df_diff.iloc[i, j] < 0:
                    brush = QtGui.QBrush(QtGui.QColor(0, 250, 154))  # 绿色
                else:
                    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))  # 白色

                item_chg.setBackground(brush)
                item_mhr.setBackground(brush)
                model_chg.setItem(i, j, item_chg)
                model_mhr.setItem(i, j, item_mhr)

    def init_table_nrc(self):
        """初始化表格及数据"""
        for tr, table in self.tableviews.items():
            model = QtGui.QStandardItemModel()
            model.setHorizontalHeaderLabels(self.tb_header_nrc)
            table.setModel(model)
            h_header = table.horizontalHeader()

            # 设置表格标题
            h_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
            h_header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

            # 设置表格视图的水平标题右击弹出菜单
            h_header.setContextMenuPolicy(Qt.CustomContextMenu)
            h_header.customContextMenuRequested.connect(lambda pos: self.show_table_header_menu(table, pos))

            # 设置槽函数
            table.doubleClicked.connect(self.tbv_tr_double_clicked)

            self.update_table_nrc(tr, table)

    def update_table_nrc(self, tr, table: QtWidgets.QTableView, filter_str=None):
        model = table.model()
        model.removeRows(0, model.rowCount())
        if filter_str:
            sql = f"""SELECT nrc_id,ref_task,description,area,status,total,remark,
                             min(report_date) as added_on,max(report_date) as latest_date
                      FROM MhNrcReport
                      WHERE register=:register AND SUBSTR(nrc_id,1,2)=:proj_id AND trade=:trade 
                            AND report_date<=:report_date AND {filter_str}
                      GROUP BY nrc_id
                      ORDER BY nrc_id ASC"""
        else:
            sql = f"""SELECT nrc_id,ref_task,description,area,status,total,remark,
                             min(report_date) as added_on,max(report_date) as latest_date
                      FROM MhNrcReport
                      WHERE register=:register AND SUBSTR(nrc_id,1,2)=:proj_id AND trade=:trade 
                            AND report_date<=:report_date
                      GROUP BY nrc_id
                      ORDER BY nrc_id ASC"""
        # 获取最新日期的报告
        self.query.prepare(sql)
        self.query.bindValue(":register", self.register)
        self.query.bindValue(":proj_id", self.proj_id)
        self.query.bindValue(":trade", tr)
        self.query.bindValue(":report_date", self.report_date)
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
                color = QtGui.QColor(0, 250, 154)  # 绿色
            else:
                color = QtGui.QColor(255, 255, 255)  # 白色
            brush = QtGui.QBrush(color)
            item.setBackground(brush)

    def init_history_table(self):
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(self.tb_header_history)
        self.ui.tbvHistory.setModel(model)
        # 设置表格标题
        h_header = self.ui.tbvHistory.horizontalHeader()
        h_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        h_header.setSectionResizeMode(self.tb_header_history.index('Description'), QtWidgets.QHeaderView.Stretch)

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


class NrcReportDetailWin(QtWidgets.QWidget):
    tb_header_subtask = ['Item_No', 'Description', 'Mhr', 'Trade', ]
    tb_mhCxRemark_mapping = {'id': 'Id',
                             'mh_id': 'Mh_Id',
                             'remark': 'Remark',
                             'create_user': 'Create_User',
                             'create_datetime': 'Create_Datetime',
                             'update_user': 'Update_User',
                             'update_datetime': 'Update_Datetime',
                             }

    def __init__(self, register, nrc_id, parent=None):
        super().__init__(parent)
        self.register = register
        self.nrc_id = nrc_id
        self.db = DatabaseManager()
        self.query = QtSql.QSqlQuery(self.db.con)
        self.tb_nrc_report = "MhNrcReport"
        self.tb_nrc_subtask = "MhSubtask"
        self.tb_mhCxRemark = "MhCxRemark"

        self.ui = Ui_NrcReportDetailForm()
        self.ui.setupUi(self)

        self.setWindowTitle(f'Manhour Detail - {nrc_id}')

        # 设置报告日期和desc
        dt = []
        desc = []
        sql = f"""SELECT description,report_date
                    FROM {self.tb_nrc_report}
                    WHERE nrc_id=:nrc_id
                    ORDER BY report_date DESC;
                    """
        self.query.prepare(sql)
        self.query.bindValue(":nrc_id", nrc_id)
        self.query.exec()
        while self.query.next():
            dt.append(self.query.value('report_date'))
            desc.append(self.query.value('description'))
        if len(dt) > 1:
            cur_date, last_date = dt[0], dt[1]
        else:
            cur_date, last_date = dt[0], dt[0]
        self.ui.dateEditToday.setDate(QDate(*[int(x) for x in cur_date.split('-')]))
        self.ui.dateEditPast.setDate(QDate(*[int(x) for x in last_date.split('-')]))
        self.ui.plainTextEditDesc.setPlainText(desc[0])

        # 更新Subtask表格数据
        cur_date = self.ui.dateEditToday.date().toString("yyyy-MM-dd")
        cur_total_mhr = self.init_table_subtask(self.ui.tbvSubtaskLatest, cur_date)
        self.ui.lineEditSbtTotalCurrent.setText(f"{cur_total_mhr:.2f}")
        self.init_table_cxRemark()

    @pyqtSlot()
    def on_btnExport_clicked(self):
        today = QDateTime.currentDateTime().toString('yyyy_MM_dd_hh_mm_ss')
        filename = f'MH_CX_REMARK_{today}.xlsx'
        save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", filename, "Excel Files (*.xlsx *.xls)")
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
        sel_model = self.sel_model_remark
        selected_indexes = sel_model.selectedRows(column=self.remark_field_num['id'])
        if not selected_indexes:
            QtWidgets.QMessageBox.information(self, 'Information', 'No row(s) selected!')
            return
        choose = QtWidgets.QMessageBox.warning(self, 'Warning', 'Are you sure to delete?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choose == QtWidgets.QMessageBox.Yes:
            self.query.prepare(f"""DELETE FROM {self.tb_mhCxRemark} WHERE id=:id""")
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

    def on_dateEditPast_userDateChanged(self, last_date):
        last_total_mhr = self.init_table_subtask(self.ui.tbvSubtaskPast, last_date)
        self.ui.lineEditSbtTotalLast.setText(f"{last_total_mhr:.2f}")

        sql = f"""SELECT SUM(total) FROM {self.tb_nrc_report} WHERE nrc_id=:nrc_id AND report_date=:report_date"""
        self.query.prepare(sql)
        self.query.bindValue(":nrc_id", self.nrc_id)
        self.query.bindValue(":report_date", self.ui.dateEditPast.date().toString('yyyy-MM-dd'))
        self.query.exec()
        if self.query.first() and self.query.value(0):
            self.ui.lineEditTotalLast.setText(f"{float(self.query.value(0)):.2f}")
        else:
            self.ui.lineEditTotalLast.setText("0.00")

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

    def init_table_subtask(self, table: QtWidgets.QTableView, report_date):
        h_header = table.horizontalHeader()
        # 创建数据模型
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(self.tb_header_subtask)
        table.setModel(model)
        h_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        h_header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        # 设置表格视图的水平标题右击弹出菜单
        h_header.setContextMenuPolicy(Qt.CustomContextMenu)
        h_header.customContextMenuRequested.connect(
            lambda pos: self.show_table_header_menu(table, pos))

        # 更新表格数据
        return self.update_table_subtask_data(table, report_date)

    def update_table_subtask_data(self, table: QtWidgets.QTableView, report_date):
        total_mhr = 0
        fields = ['item_no', 'description', 'mhr', 'trade', ]
        model: QtGui.QStandardItemModel = table.model()
        proj_id, jsn = self.nrc_id[:2], self.nrc_id[2:6]
        sql = f"""SELECT item_no,description,mhr,trade
                  FROM {self.tb_nrc_subtask}
                  WHERE register=:register AND proj_id=:proj_id AND jsn=:jsn AND report_date=:dt
                  """
        self.query.prepare(sql)
        self.query.bindValue(":register", self.register)
        self.query.bindValue(":proj_id", proj_id)
        self.query.bindValue(":jsn", jsn)
        self.query.bindValue(":dt", report_date)
        self.query.exec()
        while self.query.next():
            temp = []
            for field in fields:
                if field == 'mhr':
                    mhr = self.query.value(field)
                    total_mhr += mhr
                    item = QtGui.QStandardItem(f"{mhr:.2f}")
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                elif field == 'item_no':
                    item = QtGui.QStandardItem(str(self.query.value(field)))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                else:
                    item = QtGui.QStandardItem(str(self.query.value(field)))
                temp.append(item)
            model.appendRow(temp)

        # 获取report内工时
        sql = f"""SELECT SUM(total) FROM {self.tb_nrc_report} WHERE nrc_id=:nrc_id AND report_date=:report_date"""
        self.query.prepare(sql)
        self.query.bindValue(":nrc_id", self.nrc_id)
        self.query.bindValue(":report_date", self.ui.dateEditToday.date().toString('yyyy-MM-dd'))
        self.query.exec()
        if self.query.first():
            self.ui.lineEditTotalCurrent.setText(f"{float(self.query.value(0)):.2f}")
        else:
            self.ui.lineEditTotalCurrent.setText("0.00")

        return total_mhr

    def init_table_cxRemark(self):
        h_header = self.ui.tbvCxRemark.horizontalHeader()

        # 创建表格模型(不可编辑, 默认可排序)
        self.tb_remark_model = QtSql.QSqlTableModel(self, self.db.con)
        self.tb_remark_model.setTable(self.tb_mhCxRemark)

        # 创建选择模型
        self.sel_model_remark = QtCore.QItemSelectionModel(self.tb_remark_model)

        # 设置表格数据模型和选择模型
        self.ui.tbvCxRemark.setModel(self.tb_remark_model)
        self.ui.tbvCxRemark.setSelectionModel(self.sel_model_remark)

        # 设置表格标题
        self.remark_field_num = self.db.get_field_num(self.tb_remark_model)  # 获取字段名和序号
        for field, column in self.remark_field_num.items():  # 设置字段显示名
            self.tb_remark_model.setHeaderData(column, Qt.Horizontal, self.tb_mhCxRemark_mapping[field])

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
