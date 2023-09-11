import os
from pathlib import Path
import pandas as pd
from PyQt5 import QtWidgets, QtSql, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSlot, QDateTime

from ..ui import Ui_NrcStandardForm
from windows.image_viewer import ImageViewer
from utils.database import DatabaseManager


class NrcStandardItemWin(QtWidgets.QWidget):
    tb_header_mapping = {'item_no': 'Item_NO',
                         'ac_type': 'AC_Type',
                         'description': 'Description',
                         'work_area': 'Work_Area'}

    def __init__(self, parent=None):
        super(NrcStandardItemWin, self).__init__(parent)
        self.is_saved = True
        self.db = DatabaseManager()
        self.query = QtSql.QSqlQuery(self.db.con)
        self.tb_item_name = 'MhNrcStandardItem'
        self.tb_item_max = 'MhNrcStandardMax'
        self.tb_item_min = 'MhNrcStandardMin'
        self.tb_item_remark = 'MhNrcStandardRemark'
        self.tb_item_image = 'MhNrcStandardRemark'
        self.new_ims = []

        self.ui = Ui_NrcStandardForm()
        self.ui.setupUi(self)
        self.init_table()

        # 绑定槽函数
        self.ui.doubleSpinBoxAIMin.valueChanged.connect(self.set_total_mhr)
        self.ui.doubleSpinBoxAIMax.valueChanged.connect(self.set_total_mhr)
        self.ui.doubleSpinBoxAEMin.valueChanged.connect(self.set_total_mhr)
        self.ui.doubleSpinBoxAEMax.valueChanged.connect(self.set_total_mhr)
        self.ui.doubleSpinBoxAVMin.valueChanged.connect(self.set_total_mhr)
        self.ui.doubleSpinBoxAVMax.valueChanged.connect(self.set_total_mhr)
        self.ui.doubleSpinBoxGWMin.valueChanged.connect(self.set_total_mhr)
        self.ui.doubleSpinBoxGWMax.valueChanged.connect(self.set_total_mhr)
        self.ui.doubleSpinBoxPTMin.valueChanged.connect(self.set_total_mhr)
        self.ui.doubleSpinBoxPTMax.valueChanged.connect(self.set_total_mhr)
        self.ui.doubleSpinBoxSMMin.valueChanged.connect(self.set_total_mhr)
        self.ui.doubleSpinBoxSMMax.valueChanged.connect(self.set_total_mhr)
        self.ui.doubleSpinBoxCLMin.valueChanged.connect(self.set_total_mhr)
        self.ui.doubleSpinBoxCLMax.valueChanged.connect(self.set_total_mhr)
        self.ui.doubleSpinBoxSSMin.valueChanged.connect(self.set_total_mhr)
        self.ui.doubleSpinBoxSSMax.valueChanged.connect(self.set_total_mhr)
        self.ui.lineEditSearchDesc.returnPressed.connect(self.on_btnSearch_clicked)

    def on_tbvNrcItem_clicked(self, index: QtCore.QModelIndex):
        # 重置编辑控件为不可编辑
        self.set_editorWidget_readOnly(True)
        self.ui.cbbAcType.setEnabled(False)
        self.ui.cbbWorkArea.setEnabled(False)

        # 查询数据并设置到编辑控件中
        item_no = self.model.index(index.row(), self.field_num['item_no']).data()
        sql = """SELECT item.*,
                        mh_min.ai AS ai_min,
                        mh_min.ae AS ae_min,
                        mh_min.av AS av_min,
                        mh_min.ss AS ss_min,
                        mh_min.pt AS pt_min,
                        mh_min.sm AS sm_min,
                        mh_min.gw AS gw_min,
                        mh_min.cl AS cl_min,
                        mh_max.ai AS ai_max,
                        mh_max.ae AS ae_max,
                        mh_max.av AS av_max,
                        mh_max.ss AS ss_max,
                        mh_max.pt AS pt_max,
                        mh_max.sm AS sm_max,
                        mh_max.gw AS gw_max,
                        mh_max.cl AS cl_max,
                        rmk.remark
                FROM MhNrcStandardItem AS item
                LEFT JOIN MhNrcStandardMin AS mh_min ON mh_min.item_no=item.item_no
                LEFT JOIN MhNrcStandardMax AS mh_max ON mh_max.item_no=item.item_no
                LEFT JOIN MhNrcStandardRemark AS rmk ON rmk.item_no=item.item_no
                WHERE item.item_no=:item_no"""

        self.query.prepare(sql)
        self.query.bindValue(':item_no', item_no)
        self.query.exec()
        self.query.first()
        self.ui.lineEditIemNo.setText(self.query.value('item_no'))
        self.ui.cbbAcType.setCurrentText(self.query.value('ac_type'))
        self.ui.cbbWorkArea.setCurrentText(self.query.value('work_area'))
        self.ui.lineEditDesc.setText(self.query.value('description'))
        self.ui.doubleSpinBoxAIMin.setValue(self.query.value('ai_min'))
        self.ui.doubleSpinBoxAIMax.setValue(self.query.value('ai_max'))
        self.ui.doubleSpinBoxAEMin.setValue(self.query.value('ae_min'))
        self.ui.doubleSpinBoxAEMax.setValue(self.query.value('ae_max'))
        self.ui.doubleSpinBoxAVMin.setValue(self.query.value('av_min'))
        self.ui.doubleSpinBoxAVMax.setValue(self.query.value('av_max'))
        self.ui.doubleSpinBoxGWMin.setValue(self.query.value('gw_min'))
        self.ui.doubleSpinBoxGWMax.setValue(self.query.value('gw_max'))
        self.ui.doubleSpinBoxPTMin.setValue(self.query.value('pt_min'))
        self.ui.doubleSpinBoxPTMax.setValue(self.query.value('pt_max'))
        self.ui.doubleSpinBoxSMMin.setValue(self.query.value('sm_min'))
        self.ui.doubleSpinBoxSMMax.setValue(self.query.value('sm_max'))
        self.ui.doubleSpinBoxCLMin.setValue(self.query.value('cl_min'))
        self.ui.doubleSpinBoxCLMax.setValue(self.query.value('cl_max'))
        self.ui.doubleSpinBoxSSMin.setValue(self.query.value('ss_min'))
        self.ui.doubleSpinBoxSSMax.setValue(self.query.value('ss_max'))
        self.ui.plainTextEditRemark.setPlainText(self.query.value('remark'))

    def on_tbvNrcItem_doubleClicked(self, index):
        self.set_editorWidget_readOnly(False)
        self.ui.cbbAcType.setEnabled(True)
        self.ui.cbbWorkArea.setEnabled(True)

    @pyqtSlot()
    def on_btnSearch_clicked(self):
        condition = {}
        if self.ui.cbbSearchAcType.currentText():
            condition['ac_type'] = self.ui.cbbSearchAcType.currentText()
        if self.ui.lineEditSearchDesc.text():
            condition['description'] = self.ui.lineEditSearchDesc.text()

        filter_str = ' AND '.join([f"{field} LIKE '%{v}%'" for field, v in condition.items()])
        self.model.setFilter(filter_str)
        self.model.select()

    @pyqtSlot()
    def on_btnImport_clicked(self):
        read_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, filter="Excel Files (*.xlsx *.xls)")
        if not read_path:
            return
        self.query.exec(F"SELECT * FROM {self.tb_item_name} LIMIT 1")
        header_1 = [self.tb_header_mapping[self.query.record().fieldName(i)]
                    for i in range(self.query.record().count())]
        header_2 = ['AE_MIN', 'AE_MAX', 'AI_MIN', 'AI_MAX', 'AV_MIN', 'AV_MAX', 'CL_MIN', 'CL_MAX',
                    'GW_MIN', 'GW_MAX', 'PT_MIN', 'PT_MAX', 'SM_MIN', 'SM_MAX', 'SS_MIN', 'SS_MAX',
                    'Remark']
        header = header_1 + header_2

        df = pd.read_excel(read_path, nrows=0)
        # 验证数据字段完整性
        for x in header:
            if x not in df.columns:
                QtWidgets.QMessageBox.critical(self, 'Error', f'Column `{x}` not found in excel!')
                return
        # 读取并保存数据
        converters = {'AE_MIN': lambda y: f'{y:.2f}',
                      'AE_MAX': lambda y: f'{y:.2f}',
                      'AI_MIN': lambda y: f'{y:.2f}',
                      'AI_MAX': lambda y: f'{y:.2f}',
                      'AV_MIN': lambda y: f'{y:.2f}',
                      'AV_MAX': lambda y: f'{y:.2f}',
                      'CL_MIN': lambda y: f'{y:.2f}',
                      'CL_MAX': lambda y: f'{y:.2f}',
                      'GW_MIN': lambda y: f'{y:.2f}',
                      'GW_MAX': lambda y: f'{y:.2f}',
                      'PT_MIN': lambda y: f'{y:.2f}',
                      'PT_MAX': lambda y: f'{y:.2f}',
                      'SM_MIN': lambda y: f'{y:.2f}',
                      'SM_MAX': lambda y: f'{y:.2f}',
                      'SS_MIN': lambda y: f'{y:.2f}',
                      'SS_MAX': lambda y: f'{y:.2f}',
                      }
        df = pd.read_excel(read_path, keep_default_na=False, converters=converters)
        self.db.con.transaction()
        for i in range(df.shape[0]):
            if df.loc[i, 'Item_NO'] == "":
                item_no = self.get_next_itemNo()
            else:
                item_no = df.loc[i, 'Item_NO']
            # 更新item表
            sql = f"REPLACE INTO {self.tb_item_name} VALUES (:item_no,:ac_type,:description,:work_area)"
            self.query.prepare(sql)
            self.query.bindValue(':item_no', item_no)
            self.query.bindValue(':ac_type', df.loc[i, 'AC_Type'])
            self.query.bindValue(':description', df.loc[i, 'Description'])
            self.query.bindValue(':work_area', df.loc[i, 'Work_Area'])
            if not self.query.exec():
                self.db.con.rollback()
                QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
                return
            # 更新工时最小表
            sql = f"REPLACE INTO {self.tb_item_min} VALUES (:item_no,:ai,:ae,:av,:ss,:pt,:sm,:gw,:cl)"
            self.query.prepare(sql)
            self.query.bindValue(':item_no', item_no)
            self.query.bindValue(':ai', df.loc[i, 'AI_MIN'])
            self.query.bindValue(':ae', df.loc[i, 'AE_MIN'])
            self.query.bindValue(':av', df.loc[i, 'AV_MIN'])
            self.query.bindValue(':ss', df.loc[i, 'SS_MIN'])
            self.query.bindValue(':pt', df.loc[i, 'PT_MIN'])
            self.query.bindValue(':sm', df.loc[i, 'SM_MIN'])
            self.query.bindValue(':gw', df.loc[i, 'GW_MIN'])
            self.query.bindValue(':cl', df.loc[i, 'CL_MIN'])
            if not self.query.exec():
                self.db.con.rollback()
                QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
                return
            # 更新工时最大表
            sql = f"REPLACE INTO {self.tb_item_max} VALUES (:item_no,:ai,:ae,:av,:ss,:pt,:sm,:gw,:cl)"
            self.query.prepare(sql)
            self.query.bindValue(':item_no', item_no)
            self.query.bindValue(':ai', df.loc[i, 'AI_MAX'])
            self.query.bindValue(':ae', df.loc[i, 'AE_MAX'])
            self.query.bindValue(':av', df.loc[i, 'AV_MAX'])
            self.query.bindValue(':ss', df.loc[i, 'SS_MAX'])
            self.query.bindValue(':pt', df.loc[i, 'PT_MAX'])
            self.query.bindValue(':sm', df.loc[i, 'SM_MAX'])
            self.query.bindValue(':gw', df.loc[i, 'GW_MAX'])
            self.query.bindValue(':cl', df.loc[i, 'CL_MAX'])
            if not self.query.exec():
                self.db.con.rollback()
                QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
                return
            # 保存remark
            sql = f"REPLACE INTO {self.tb_item_remark} VALUES (:item_no,:remark)"
            self.query.prepare(sql)
            self.query.bindValue(':item_no', item_no)
            self.query.bindValue(':remark', df.loc[i, 'Remark'])
            if not self.query.exec():
                QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
                self.db.con.rollback()
                return

        self.db.con.commit()
        QtWidgets.QMessageBox.information(self, 'Information', 'Import successfully!')

    @pyqtSlot()
    def on_btnExport_clicked(self):
        today = QDateTime.currentDateTime().toString('yyyy_MM_dd_hh_mm_ss')
        filename = f'MH_NRC_STANDARD_{today}.xlsx'
        save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", filename, "Excel Files (*.xlsx *.xls)")
        if not save_path:
            return

        save_path = Path(save_path).resolve()
        # 创建工时记录DataFrame对象
        self.query.exec("SELECT * FROM MhNrcStandardItem")
        data = []
        header_1 = [self.tb_header_mapping[self.query.record().fieldName(i)]
                    for i in range(self.query.record().count())]
        header_2 = ['AE_MIN', 'AE_MAX', 'AI_MIN', 'AI_MAX', 'AV_MIN', 'AV_MAX', 'CL_MIN', 'CL_MAX',
                    'GW_MIN', 'GW_MAX', 'PT_MIN', 'PT_MAX', 'SM_MIN', 'SM_MAX', 'SS_MIN', 'SS_MAX',
                    'Remark']
        header = header_1 + header_2
        sql = """SELECT item.*,
                                mh_min.ai AS ai_min,
                                mh_min.ae AS ae_min,
                                mh_min.av AS av_min,
                                mh_min.ss AS ss_min,
                                mh_min.pt AS pt_min,
                                mh_min.sm AS sm_min,
                                mh_min.gw AS gw_min,
                                mh_min.cl AS cl_min,
                                mh_max.ai AS ai_max,
                                mh_max.ae AS ae_max,
                                mh_max.av AS av_max,
                                mh_max.ss AS ss_max,
                                mh_max.pt AS pt_max,
                                mh_max.sm AS sm_max,
                                mh_max.gw AS gw_max,
                                mh_max.cl AS cl_max,
                                rmk.remark
                        FROM MhNrcStandardItem AS item
                        LEFT JOIN MhNrcStandardMin AS mh_min ON mh_min.item_no=item.item_no
                        LEFT JOIN MhNrcStandardMax AS mh_max ON mh_max.item_no=item.item_no
                        LEFT JOIN MhNrcStandardRemark AS rmk ON rmk.item_no=item.item_no
                        WHERE item.item_no=:item_no"""
        self.query.prepare(sql)
        for i in range(self.model.rowCount()):
            row_data = []
            item_no = self.model.index(i, self.field_num['item_no']).data()
            for j in range(self.model.columnCount()):
                row_data.append(self.model.data(self.model.index(i, j), Qt.DisplayRole))
            # 加入工时数据和remark数据
            self.query.bindValue(':item_no', item_no)
            self.query.exec()
            self.query.first()
            for h in header_2:
                row_data.append(self.query.value(h.lower()))
            data.append(row_data)  # 将行数据添加到data列表中
        df = pd.DataFrame(data, columns=header)
        df.to_excel(save_path, index=False)
        # 打开保存文件夹
        os.startfile(save_path.parent)

    @pyqtSlot()
    def on_btnNew_clicked(self):
        # 设置编辑控件可编辑
        self.ui.cbbAcType.setEnabled(True)
        self.ui.cbbWorkArea.setEnabled(True)
        self.ui.btnNewImage.setEnabled(True)
        self.set_editorWidget_readOnly(False)
        self.reset_editorWidget_value()
        self.get_next_itemNo()

    @pyqtSlot()
    def on_btnAddImage_clicked(self):
        sel_idxes = self.selection_model.selectedRows(column=self.field_num['item_no'])
        if not sel_idxes:
            QtWidgets.QMessageBox.information(self, 'Information', 'No row(s) selected!')
            return

        file_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Open Image", "",
                                                               "Image Files (*.png *.jpg *.bmp)")
        if not file_paths:
            return

        sql = """INSERT INTO MhNrcStandardImage
                 VALUES (:id,:item_no,:name,:image,(SELECT IFNULL(MAX(sheet)+1,1) 
                                                    FROM MhNrcStandardImage WHERE item_no=:item_no))"""
        self.db.con.transaction()  # 创建事务
        self.query.prepare(sql)
        for file_path in file_paths:
            with open(file_path, 'rb') as f:
                image_data = QtCore.QByteArray(f.read())  # 以二进制模式打开图片数据并转化为QByteArray对象
            path = Path(file_path)
            for index in sel_idxes:
                self.query.bindValue(':id', None)
                self.query.bindValue(':item_no', index.data())
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
        sel_idxes = self.selection_model.selectedRows(column=self.field_num['item_no'])
        if len(sel_idxes) != 1:
            QtWidgets.QMessageBox.information(self, 'Information', 'One row should be selected!')
            return
        ims = []
        item_no = sel_idxes[0].data()
        sql = "SELECT id,sheet,name,image FROM MhNrcStandardImage WHERE item_no=:item_no ORDER BY sheet ASC"
        self.query.prepare(sql)
        self.query.bindValue(':item_no', item_no)
        self.query.exec()
        while self.query.next():
            ims.append({field: self.query.value(field) for field in ['id', 'sheet', 'name', 'image']})
        if not ims:
            QtWidgets.QMessageBox.information(self, 'Information', 'No images')
            return

        self.image_viewer = ImageViewer('MhNrcStandardImage', ims)
        self.image_viewer.show()
        self.image_viewer.fit_image()

    @pyqtSlot()
    def on_btnDelete_clicked(self):
        sel_idxes = self.selection_model.selectedRows(self.field_num['item_no'])
        if not sel_idxes:
            QtWidgets.QMessageBox.information(self, 'Information', 'No rows selected')
            return
        options = QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        choose = QtWidgets.QMessageBox.warning(self, 'Warning', 'Do you want to Delete?', options)
        if choose == QtWidgets.QMessageBox.No:
            return
        tables = [self.tb_item_name, self.tb_item_min, self.tb_item_max, self.tb_item_remark, self.tb_item_image]
        self.db.con.transaction()
        for table in tables:
            self.query.prepare(f"""DELETE FROM {table} WHERE item_no=:item_no""")
            for idx in sel_idxes:
                self.query.bindValue(':item_no', idx.data())
                if not self.query.exec():
                    QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
                    self.db.con.rollback()
                    return
        self.db.con.commit()
        QtWidgets.QMessageBox.information(self, 'Information', 'Deleted successfully')
        self.on_btnSearch_clicked()

    @pyqtSlot()
    def on_btnNewImage_clicked(self):
        file_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Open Image", "",
                                                               "Image Files (*.png *.jpg *.bmp)")
        if not file_paths:
            return
        self.new_ims = file_paths

    @pyqtSlot()
    def on_btnSave_clicked(self):
        # 检查输入数据
        item_no = self.ui.lineEditIemNo.text()
        ac_type = self.ui.cbbAcType.currentText()
        work_area = self.ui.cbbWorkArea.currentText()
        desc = self.ui.lineEditDesc.text()
        if not ac_type or not work_area or not desc:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'AC Type, Work Area and Description empty found!')
            return
        # 启动数据库事务
        self.db.con.transaction()
        # 保存项目信息
        sql = f"""REPLACE INTO {self.tb_item_name} VALUES (:item_no,:ac_type,:description,:work_area)"""
        self.query.prepare(sql)
        self.query.bindValue(':item_no', item_no)
        self.query.bindValue(':ac_type', ac_type)
        self.query.bindValue(':description', desc)
        self.query.bindValue(':work_area', work_area)

        if not self.query.exec():
            QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
            self.db.con.rollback()
            return

        # 保存工时信息-最小值
        sql = f"""REPLACE INTO {self.tb_item_min} VALUES (:item_no,:ai,:ae,:av,:ss,:pt,:sm,:gw,:cl)"""
        self.query.prepare(sql)
        self.query.bindValue(':item_no', item_no)
        self.query.bindValue(':ai', self.ui.doubleSpinBoxAIMin.value())
        self.query.bindValue(':ae', self.ui.doubleSpinBoxAEMin.value())
        self.query.bindValue(':av', self.ui.doubleSpinBoxAVMin.value())
        self.query.bindValue(':ss', self.ui.doubleSpinBoxSSMin.value())
        self.query.bindValue(':pt', self.ui.doubleSpinBoxPTMin.value())
        self.query.bindValue(':sm', self.ui.doubleSpinBoxSMMin.value())
        self.query.bindValue(':gw', self.ui.doubleSpinBoxGWMin.value())
        self.query.bindValue(':cl', self.ui.doubleSpinBoxCLMin.value())
        if not self.query.exec():
            QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
            self.db.con.rollback()
            return

        # 保存工时信息-最大值
        sql = f"""REPLACE INTO {self.tb_item_max} VALUES (:item_no,:ai,:ae,:av,:ss,:pt,:sm,:gw,:cl)"""
        self.query.prepare(sql)
        self.query.bindValue(':item_no', item_no)
        self.query.bindValue(':ai', self.ui.doubleSpinBoxAIMax.value())
        self.query.bindValue(':ae', self.ui.doubleSpinBoxAEMax.value())
        self.query.bindValue(':av', self.ui.doubleSpinBoxAVMax.value())
        self.query.bindValue(':ss', self.ui.doubleSpinBoxSSMax.value())
        self.query.bindValue(':pt', self.ui.doubleSpinBoxPTMax.value())
        self.query.bindValue(':sm', self.ui.doubleSpinBoxSMMax.value())
        self.query.bindValue(':gw', self.ui.doubleSpinBoxGWMax.value())
        self.query.bindValue(':cl', self.ui.doubleSpinBoxCLMax.value())
        if not self.query.exec():
            QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
            self.db.con.rollback()
            return

        # 保存remark
        sql = f"""REPLACE INTO {self.tb_item_remark} VALUES (:item_no,:remark)"""
        self.query.prepare(sql)
        self.query.bindValue(':item_no', item_no)
        self.query.bindValue(':remark', self.ui.plainTextEditRemark.toPlainText())
        if not self.query.exec():
            QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
            self.db.con.rollback()
            return

        # 保存图片
        sql = """INSERT INTO MhNrcStandardImage
                 VALUES (:id,:item_no,:name,:image,(SELECT IFNULL(MAX(sheet)+1,1) 
                                                    FROM MhNrcStandardImage WHERE item_no=:item_no))"""
        self.query.prepare(sql)
        for im in self.new_ims:
            with open(im, 'rb') as f:
                image_data = QtCore.QByteArray(f.read())  # 以二进制模式打开图片数据并转化为QByteArray对象
            path = Path(im)
            self.query.bindValue(':id', None)
            self.query.bindValue(':item_no', item_no)
            self.query.bindValue(':name', path.name)
            self.query.bindValue(':image', image_data)
            if not self.query.exec():
                self.db.con.rollback()
                QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
                return

        self.db.con.commit()
        QtWidgets.QMessageBox.information(self, 'Information', 'Saved.')
        self.on_btnSearch_clicked()

        # 设置编辑控件不可编辑
        self.new_ims = []
        self.ui.cbbAcType.setEnabled(False)
        self.ui.cbbWorkArea.setEnabled(False)
        self.set_editorWidget_readOnly(True)
        self.reset_editorWidget_value()
        self.ui.btnSave.setEnabled(False)
        self.ui.btnNewImage.setEnabled(False)

    def init_table(self):
        h_header = self.ui.tbvNrcItem.horizontalHeader()

        # 创建表格模型(不可编辑, 默认可排序)
        self.model = QtSql.QSqlRelationalTableModel(self, self.db.con)
        # self.model = QtSql.QSqlTableModel(self, self.db.con)
        self.model.setTable(self.tb_item_name)
        self.model.setRelation(0, QtSql.QSqlRelation(self.tb_item_min, "item_no", "item_no"))
        self.model.setRelation(0, QtSql.QSqlRelation(self.tb_item_max, "item_no", "item_no"))
        self.model.setRelation(0, QtSql.QSqlRelation(self.tb_item_remark, "item_no", "item_no"))
        self.model.setRelation(0, QtSql.QSqlRelation(self.tb_item_image, "item_no", "item_no"))

        # 创建选择模型
        self.selection_model = QtCore.QItemSelectionModel(self.model)

        # 设置表格数据模型和选择模型
        self.ui.tbvNrcItem.setModel(self.model)
        self.ui.tbvNrcItem.setSelectionModel(self.selection_model)

        # 设置表格标题
        self.field_num = self.db.get_field_num(self.model)  # 获取字段名和序号
        for field, column in self.field_num.items():  # 设置字段显示名
            self.model.setHeaderData(column, Qt.Horizontal, self.tb_header_mapping[field])

        # 设置表格视图属性
        for field, column in self.field_num.items():  # 设置表格列宽度默认行为
            if field in ['description']:
                h_header.setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)
            else:
                h_header.setSectionResizeMode(column, QtWidgets.QHeaderView.ResizeToContents)
            if field in ['item_no', 'work_area']:
                self.ui.tbvNrcItem.hideColumn(column)

        # 设置表格视图的水平标题右击弹出菜单
        h_header.setContextMenuPolicy(Qt.CustomContextMenu)
        h_header.customContextMenuRequested.connect(lambda pos: self.show_table_header_menu(self.ui.tbvNrcItem, pos))

        self.ui.cbbAcType.currentTextChanged.connect(lambda: self.ui.btnSave.setEnabled(True))
        self.ui.cbbWorkArea.currentTextChanged.connect(lambda: self.ui.btnSave.setEnabled(True))
        self.ui.doubleSpinBoxAIMin.textChanged.connect(lambda: self.ui.btnSave.setEnabled(True))
        self.ui.doubleSpinBoxAIMax.textChanged.connect(lambda: self.ui.btnSave.setEnabled(True))
        self.ui.doubleSpinBoxAEMin.textChanged.connect(lambda: self.ui.btnSave.setEnabled(True))
        self.ui.doubleSpinBoxAEMax.textChanged.connect(lambda: self.ui.btnSave.setEnabled(True))
        self.ui.doubleSpinBoxAVMin.textChanged.connect(lambda: self.ui.btnSave.setEnabled(True))
        self.ui.doubleSpinBoxAVMax.textChanged.connect(lambda: self.ui.btnSave.setEnabled(True))
        self.ui.doubleSpinBoxGWMin.textChanged.connect(lambda: self.ui.btnSave.setEnabled(True))
        self.ui.doubleSpinBoxGWMax.textChanged.connect(lambda: self.ui.btnSave.setEnabled(True))
        self.ui.doubleSpinBoxPTMin.textChanged.connect(lambda: self.ui.btnSave.setEnabled(True))
        self.ui.doubleSpinBoxPTMax.textChanged.connect(lambda: self.ui.btnSave.setEnabled(True))
        self.ui.doubleSpinBoxSMMin.textChanged.connect(lambda: self.ui.btnSave.setEnabled(True))
        self.ui.doubleSpinBoxSMMax.textChanged.connect(lambda: self.ui.btnSave.setEnabled(True))
        self.ui.doubleSpinBoxCLMin.textChanged.connect(lambda: self.ui.btnSave.setEnabled(True))
        self.ui.doubleSpinBoxCLMax.textChanged.connect(lambda: self.ui.btnSave.setEnabled(True))
        self.ui.doubleSpinBoxSSMin.textChanged.connect(lambda: self.ui.btnSave.setEnabled(True))
        self.ui.doubleSpinBoxSSMax.textChanged.connect(lambda: self.ui.btnSave.setEnabled(True))
        self.ui.plainTextEditRemark.textChanged.connect(lambda: self.ui.btnSave.setEnabled(True))

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

    def set_editorWidget_readOnly(self, r=True):
        self.ui.lineEditDesc.setReadOnly(r)
        self.ui.doubleSpinBoxAIMin.setReadOnly(r)
        self.ui.doubleSpinBoxAIMax.setReadOnly(r)
        self.ui.doubleSpinBoxAEMin.setReadOnly(r)
        self.ui.doubleSpinBoxAEMax.setReadOnly(r)
        self.ui.doubleSpinBoxAVMin.setReadOnly(r)
        self.ui.doubleSpinBoxAVMax.setReadOnly(r)
        self.ui.doubleSpinBoxGWMin.setReadOnly(r)
        self.ui.doubleSpinBoxGWMax.setReadOnly(r)
        self.ui.doubleSpinBoxPTMin.setReadOnly(r)
        self.ui.doubleSpinBoxPTMax.setReadOnly(r)
        self.ui.doubleSpinBoxSMMin.setReadOnly(r)
        self.ui.doubleSpinBoxSMMax.setReadOnly(r)
        self.ui.doubleSpinBoxCLMin.setReadOnly(r)
        self.ui.doubleSpinBoxCLMax.setReadOnly(r)
        self.ui.doubleSpinBoxSSMin.setReadOnly(r)
        self.ui.doubleSpinBoxSSMax.setReadOnly(r)
        self.ui.plainTextEditRemark.setReadOnly(r)

    def reset_editorWidget_value(self):
        self.ui.doubleSpinBoxAIMin.setValue(0.0)
        self.ui.doubleSpinBoxAIMax.setValue(0.0)
        self.ui.doubleSpinBoxAEMin.setValue(0.0)
        self.ui.doubleSpinBoxAEMax.setValue(0.0)
        self.ui.doubleSpinBoxAVMin.setValue(0.0)
        self.ui.doubleSpinBoxAVMax.setValue(0.0)
        self.ui.doubleSpinBoxGWMin.setValue(0.0)
        self.ui.doubleSpinBoxGWMax.setValue(0.0)
        self.ui.doubleSpinBoxPTMin.setValue(0.0)
        self.ui.doubleSpinBoxPTMax.setValue(0.0)
        self.ui.doubleSpinBoxSMMin.setValue(0.0)
        self.ui.doubleSpinBoxSMMax.setValue(0.0)
        self.ui.doubleSpinBoxCLMin.setValue(0.0)
        self.ui.doubleSpinBoxCLMax.setValue(0.0)
        self.ui.doubleSpinBoxSSMin.setValue(0.0)
        self.ui.doubleSpinBoxSSMax.setValue(0.0)
        self.ui.cbbAcType.setCurrentText('')
        self.ui.cbbWorkArea.setCurrentText('')
        self.ui.lineEditDesc.setText('')
        self.ui.lineEditIemNo.setText('')
        self.ui.plainTextEditRemark.setPlainText('')

    def set_total_mhr(self):
        total_min = sum([self.ui.doubleSpinBoxAIMin.value(),
                         self.ui.doubleSpinBoxAEMin.value(),
                         self.ui.doubleSpinBoxAVMin.value(),
                         self.ui.doubleSpinBoxGWMin.value(),
                         self.ui.doubleSpinBoxPTMin.value(),
                         self.ui.doubleSpinBoxSMMin.value(),
                         self.ui.doubleSpinBoxCLMin.value(),
                         self.ui.doubleSpinBoxSSMin.value(), ])
        total_max = sum([self.ui.doubleSpinBoxSSMax.value(),
                         self.ui.doubleSpinBoxAIMax.value(),
                         self.ui.doubleSpinBoxAEMax.value(),
                         self.ui.doubleSpinBoxAVMax.value(),
                         self.ui.doubleSpinBoxGWMax.value(),
                         self.ui.doubleSpinBoxPTMax.value(),
                         self.ui.doubleSpinBoxSMMax.value(),
                         self.ui.doubleSpinBoxCLMax.value(), ])
        self.ui.doubleSpinBoxTotalMin.setValue(total_min)
        self.ui.doubleSpinBoxTotalMax.setValue(total_max)

    def get_next_itemNo(self):
        sql = f"""SELECT MAX(item_no) as cur_itemNo FROM {self.tb_item_name}"""
        self.query.exec(sql)
        self.query.first()
        cur_itemNo = self.query.value(0)
        if not cur_itemNo:
            next_itemNo = 'I00001'
        else:
            next_itemNo = f"I{int(cur_itemNo[1:]) + 1:0>5}"
        self.ui.lineEditIemNo.setText(next_itemNo)
        return next_itemNo
