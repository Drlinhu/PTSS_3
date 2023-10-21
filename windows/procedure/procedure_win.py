import os
from pathlib import Path
import pandas as pd
from PyQt5 import QtWidgets, QtSql, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot, Qt, QDateTime, QItemSelectionModel, QSettings

from ..ui import Ui_ProcedureForm, Ui_NewReferenceDialog, Ui_NewIcwDialog, Ui_NewProcLabelDialog
from ..image_viewer import ImageViewer
from utils.database import DatabaseManager

settings = QSettings("config.ini", QSettings.IniFormat)


class ProcedureWin(QtWidgets.QWidget):
    tb_header_proc = {'proc_id': 'Procedure_ID',
                      'craft_code': 'CRAFT_CODE',
                      'description': 'Description',
                      'location': 'Location',
                      'action': 'Action',
                      'access': 'Access',
                      'remark': 'Remark', }
    tb_header_ref = {'id': 'ID',
                     'proc_id': 'Procedure_ID',
                     'ref': 'Reference',
                     'type': 'Type', }
    tb_header_panel = {'id': 'ID',
                       'proc_id': 'Procedure_ID',
                       'panel': 'Panel', }
    tb_header_icw = {'id': 'ID',
                     'proc_id': 'Procedure_ID',
                     'icw': 'ICW',
                     'mhr': 'MHR',
                     'remark': 'Remark', }
    tb_header_label = {'id': 'ID',
                       'proc_id': 'Procedure_ID',
                       'label': 'Label',
                       }

    def __init__(self, parent=None):
        super().__init__(parent)

        self.db = DatabaseManager()
        self.query = QtSql.QSqlQuery(self.db.con)
        self.tb_name_proc = 'Procedure'
        self.tb_name_ref = 'ProcedureRef'
        self.tb_name_panel = 'ProcedurePanel'
        self.tb_name_icw = 'ProcedureIcw'
        self.tb_name_image = 'ProcedureImage'
        self.tb_name_label = 'ProcedureLabel'
        self.save_mode = 'NEW'
        self.header_from_excel = list(self.tb_header_proc.values())
        self.new_ims = []

        self.ui = Ui_ProcedureForm()
        self.ui.setupUi(self)
        self.ui.cbbLocation.addItems(sorted([''] + settings.value("options/location")))
        self.ui.cbbActionType.addItems(sorted([''] + settings.value("options/action")))

        self.init_proc_table()  # 初始化表格
        self.init_ref_table()
        self.init_panel_table()
        self.init_icw_table()
        self.init_label_table()

        # 设置槽函数
        self.ui.lineEditSearchProcId.returnPressed.connect(self.on_btnSearchProc_clicked)
        self.ui.lineEditSearchDesc.returnPressed.connect(self.on_btnSearchProc_clicked)

    def on_tbvProc_clicked(self, idx: QtCore.QModelIndex):  # TODO
        self.set_button_enable(False)
        self.set_editor_edited(True)

        model_proc = self.ui.tbvProc.model()
        self.ui.lineEditProcId.setText(model_proc.index(idx.row(), self.field_num_proc['proc_id']).data())
        self.ui.plainTextEditDesc.setPlainText(model_proc.index(idx.row(), self.field_num_proc['description']).data())
        self.ui.cbbCraftCode.setCurrentText(model_proc.index(idx.row(), self.field_num_proc['craft_code']).data())
        self.ui.cbbLocation.setCurrentText(model_proc.index(idx.row(), self.field_num_proc['location']).data())
        self.ui.cbbActionType.setCurrentText(model_proc.index(idx.row(), self.field_num_proc['action']).data())
        self.ui.plainTextEditAccessDesc.setPlainText(model_proc.index(idx.row(), self.field_num_proc['access']).data())
        self.ui.plainTextEditRemark.setPlainText(model_proc.index(idx.row(), self.field_num_proc['remark']).data())

        # 查询并显示reference
        proc_id = model_proc.index(idx.row(), self.field_num_proc['proc_id']).data()
        self.ui.tbvReference.model().setFilter(f"proc_id='{proc_id}' ORDER BY id,proc_id ASC")
        self.ui.tbvReference.model().select()

        # 查询并显示panel
        self.ui.tbvPanel.model().setFilter(f"proc_id='{proc_id}' ORDER BY id,proc_id ASC")
        self.ui.tbvPanel.model().select()

        # 查询并显示icw
        self.ui.tbvIcw.model().setFilter(f"proc_id='{proc_id}' ORDER BY id,proc_id ASC")
        self.ui.tbvIcw.model().select()

        # 查询并显示label
        self.ui.tbvLabel.model().setFilter(f"proc_id='{proc_id}' ORDER BY id,proc_id ASC")
        self.ui.tbvLabel.model().select()

    def on_tbvProc_doubleClicked(self, idx: QtCore.QModelIndex):  # TODO
        self.save_mode = 'MODIFY'
        self.set_editor_edited(False)
        self.set_button_enable(True)

        model = self.ui.tbvProc.model()
        self.ui.lineEditProcId.setText(model.index(idx.row(), self.field_num_proc['proc_id']).data())
        self.ui.plainTextEditDesc.setPlainText(model.index(idx.row(), self.field_num_proc['description']).data())

    @pyqtSlot()
    def on_btnSearchProc_clicked(self):
        model: QtSql.QSqlTableModel = self.ui.tbvProc.model()
        condition = {}
        if self.ui.lineEditSearchProcId.text():
            condition['proc_id'] = self.ui.lineEditSearchProcId.text()
        if self.ui.lineEditSearchDesc.text():
            condition['description'] = self.ui.lineEditSearchDesc.text()
        filter_str = ' AND '.join([f"{field} LIKE '%{v}%'" for field, v in condition.items()])
        model.setFilter(filter_str)
        model.select()

    @pyqtSlot()
    def on_btnImportProc_clicked(self):
        read_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, filter="Excel Files (*.xlsx *.xls)")
        if not read_path:
            return

        # 读取数据为dataframe
        df = pd.read_excel(read_path, nrows=0)
        header_proc_revert = {v: k for k, v in self.tb_header_proc.items()}
        columns = [header_proc_revert[x] for x in df.columns]  # 读取的excel满足数据库表的列

        if not columns:
            QtWidgets.QMessageBox.critical(self, 'Error', 'No needed data found in excel.')

        # 读取并保存数据
        converters = {'Procedure_ID': lambda y: str(y).strip(),
                      'Description': lambda y: str(y).strip(),
                      'Location': lambda y: str(y).strip(),
                      'Action': lambda y: str(y).strip(),
                      'Access': lambda y: str(y).strip(),
                      'Remark': lambda y: str(y).strip(),
                      }
        df = pd.read_excel(read_path, keep_default_na=False, converters=converters)

        self.db.con.transaction()

        # 保存proc_id和description
        sql = f"""INSERT INTO {self.tb_name_proc}
                  VALUES ({','.join([f':{field}' for field in self.tb_header_proc.keys()])})
                  ON CONFLICT (proc_id) 
                  DO UPDATE SET {','.join([f"{field}=CASE WHEN {field}=:{field} THEN {field} ELSE :{field} END"
                                           for field in columns])}"""
        self.query.prepare(sql)
        for i in range(df.shape[0]):
            for field, column in self.field_num_proc.items():
                if field in columns:
                    header = self.tb_header_proc[field]
                    self.query.bindValue(f":{field}", df.loc[i, header])
                else:
                    self.query.bindValue(f":{field}", '')
            if not self.query.exec():
                self.db.con.rollback()
                QtWidgets.QMessageBox.critical(self, 'Error', f'Failed\n{self.query.lastError().text()}')
                return
        self.db.con.commit()
        QtWidgets.QMessageBox.information(self, 'Information', 'Import successfully!')
        self.on_btnSearchProc_clicked()

    @pyqtSlot()
    def on_btnExportProc_clicked(self):
        today = QDateTime.currentDateTime().toString('yyyy_MM_dd_hh_mm_ss')
        filename = f'Procedure_{today}.xlsx'
        save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", filename, "Excel Files (*.xlsx *.xls)")
        if not save_path:
            return
        save_path = Path(save_path).resolve()

        model = self.ui.tbvProc.model()

        """ 创建空的Dataframe """
        data = []
        for i in range(model.rowCount()):
            row_data = []
            for j in range(model.columnCount()):
                row_data.append(model.data(model.index(i, j), Qt.DisplayRole))
            data.append(row_data)

        df = pd.DataFrame(data=data, columns=self.header_from_excel)
        df.to_excel(save_path, index=False)

        # 打开保存文件夹
        os.startfile(save_path.parent)

    @pyqtSlot()
    def on_btnDeleteProc_clicked(self):
        sel_model = self.ui.tbvProc.selectionModel()
        sel_idxes = sel_model.selectedRows(self.field_num_proc['proc_id'])
        if not sel_idxes:
            QtWidgets.QMessageBox.information(self, 'Information', 'No rows selected')
            return
        options = QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        choose = QtWidgets.QMessageBox.warning(self, 'Warning', 'Do you want to Delete?', options)
        if choose == QtWidgets.QMessageBox.No:
            return
        tables = [self.tb_name_proc, self.tb_name_ref, self.tb_name_panel, self.tb_name_icw, self.tb_name_image]
        self.db.con.transaction()
        for table in tables:
            self.query.prepare(f"""DELETE FROM {table} WHERE proc_id=:proc_id""")
            for idx in sel_idxes:
                self.query.bindValue(':proc_id', idx.data())
                if not self.query.exec():
                    QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
                    self.db.con.rollback()
                    return
        self.db.con.commit()
        QtWidgets.QMessageBox.information(self, 'Information', 'Deleted successfully')
        self.on_btnSearchProc_clicked()

    @pyqtSlot()
    def on_btnNewProc_clicked(self):
        self.ui.lineEditProcId.setReadOnly(False)
        self.ui.plainTextEditDesc.setReadOnly(False)
        self.set_button_enable(True)

    @pyqtSlot()
    def on_btnAddImage_clicked(self):  # TODO
        sel_model = self.ui.tbvProc.selectionModel()
        sel_idxes = sel_model.selectedRows(column=self.field_num_proc['proc_id'])
        if not sel_idxes:
            QtWidgets.QMessageBox.information(self, 'Information', 'No row(s) selected!')
            return

        file_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Open Image", "",
                                                               "Image Files (*.png *.jpg *.bmp)")
        if not file_paths:
            return

        sql = f"""INSERT INTO {self.tb_name_image}
                        VALUES (:id,:proc_id,:name,:image,(SELECT IFNULL(MAX(sheet)+1,1) 
                                                           FROM {self.tb_name_image} WHERE proc_id=:proc_id))"""
        self.db.con.transaction()  # 创建事务
        self.query.prepare(sql)
        for file_path in file_paths:
            with open(file_path, 'rb') as f:
                image_data = QtCore.QByteArray(f.read())  # 以二进制模式打开图片数据并转化为QByteArray对象
            path = Path(file_path)
            for index in sel_idxes:
                self.query.bindValue(':id', None)
                self.query.bindValue(':proc_id', index.data())
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
        sel_model = self.ui.tbvProc.selectionModel()
        sel_idxes = sel_model.selectedRows(column=self.field_num_proc['proc_id'])
        if len(sel_idxes) != 1:
            QtWidgets.QMessageBox.information(self, 'Information', 'One row should be selected!')
            return
        ims = []
        proc_id = sel_idxes[0].data()
        sql = f"SELECT id,sheet,name,image FROM {self.tb_name_image} WHERE proc_id=:proc_id ORDER BY sheet ASC"
        self.query.prepare(sql)
        self.query.bindValue(':proc_id', proc_id)
        self.query.exec()
        while self.query.next():
            ims.append({field: self.query.value(field) for field in ['id', 'sheet', 'name', 'image']})
        if not ims:
            QtWidgets.QMessageBox.information(self, 'Information', 'No images')
            return

        self.image_viewer = ImageViewer(self.tb_name_image, ims)
        self.image_viewer.show()
        self.image_viewer.fit_image()

    @pyqtSlot()
    def on_toolButtonImportRef_clicked(self):
        read_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, filter="Excel Files (*.xlsx *.xls)")
        if not read_path:
            return

        # check column in excel
        columns = list(self.tb_header_ref.values())[1:]
        df = pd.read_excel(read_path, nrows=0)
        for column in columns:
            if column not in df.columns:
                QtWidgets.QMessageBox.critical(self, 'ERROR', f'{column} not found.')
                return

        # read all excel data
        df = pd.read_excel(read_path)
        sql = f"""INSERT INTO {self.tb_name_ref}
                  SELECT :id,:proc_id,:ref,:type
                  WHERE NOT EXISTS (SELECT * FROM {self.tb_name_ref} WHERE proc_id=:proc_id AND ref=:ref)"""
        self.db.con.transaction()
        self.query.prepare(sql)
        for i in range(df.shape[0]):
            self.query.bindValue(":id", None)
            self.query.bindValue(":proc_id", df.loc[i, self.tb_header_ref['proc_id']])
            self.query.bindValue(":ref", df.loc[i, self.tb_header_ref['ref']])
            self.query.bindValue(":type", df.loc[i, self.tb_header_ref['type']])
            if not self.query.exec():
                QtWidgets.QMessageBox.critical(self, 'ERROR', self.query.lastError().text())
                self.db.con.rollback()
                return
        if self.db.con.commit():
            QtWidgets.QMessageBox.information(self, 'INFO.', 'Successfully.')
        else:
            QtWidgets.QMessageBox.critical(self, 'ERROR', self.db.con.lastError().text())

    @pyqtSlot()
    def on_toolButtonExportRef_clicked(self):
        today = QDateTime.currentDateTime().toString('yyyy_MM_dd_hh_mm_ss')
        filename = f'Procedure_Reference{today}.xlsx'
        save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", filename, "Excel Files (*.xlsx)")
        if not save_path:
            return

        columns = list(self.tb_header_ref.values())[1:]
        model = self.ui.tbvReference.model()
        data = []
        for i in range(model.rowCount()):
            row_data = [model.index(i, j).data() for j in range(model.columnCount()) if j > 0]
            data.append(row_data)
        df = pd.DataFrame(data, columns=columns)
        df.to_excel(save_path, index=False)
        os.startfile(save_path)

    @pyqtSlot()
    def on_toolButtonImportPanel_clicked(self):  # TODO
        pass

    @pyqtSlot()
    def on_toolButtonExportPanel_clicked(self):  # TODO
        pass

    @pyqtSlot()
    def on_toolButtonImportIcw_clicked(self):  # TODO
        pass

    @pyqtSlot()
    def on_toolButtonExportIcw_clicked(self):  # TODO
        pass

    @pyqtSlot()
    def on_btnNewRef_clicked(self):
        sel_model = self.ui.tbvProc.selectionModel()
        sel_idxes = sel_model.selectedRows(self.field_num_proc['proc_id'])
        if len(sel_idxes) != 1:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Only one row should be selected.')
            return
        proc_id = sel_idxes[0].data()
        dialog = NewReferenceDialog(proc_id)
        dialog.exec()

        # 显示reference
        model_ref: QtSql.QSqlTableModel = self.ui.tbvReference.model()
        model_ref.setFilter(f"proc_id='{proc_id}' ORDER BY id,proc_id ASC")
        model_ref.select()

    @pyqtSlot()
    def on_btnDeleteRef_clicked(self):
        proc_id = self.ui.lineEditProcId.text()

        # 执行删除reference程序
        sel_model = self.ui.tbvReference.selectionModel()
        sel_idxes = sel_model.selectedRows(0)
        sql = f"DELETE FROM {self.tb_name_ref} WHERE id=:id"
        self.query.prepare(sql)
        self.db.con.transaction()
        for x in sel_idxes:
            self.query.bindValue(":id", x.data())
            if not self.query.exec():
                QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
                self.db.con.rollback()
                return
        self.db.con.commit()
        # 显示reference
        self.ui.tbvReference.model().setFilter(f"proc_id='{proc_id}' ORDER BY id,proc_id ASC")
        self.ui.tbvReference.model().select()

    @pyqtSlot()
    def on_btnAddImageRef_clicked(self):  # TODO
        sel_model = self.ui.tbvReference.selectionModel()
        sel_idxes = sel_model.selectedRows(column=self.field_num_ref['proc_id'])
        if not sel_idxes:
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
                # 读取图片数据并创建 QImage 对象
                q_image = QtGui.QImage.fromData(image_data)
                # 将 QImage 对象以指定格式和压缩参数保存为字节数据
                byte_array = QtCore.QByteArray()
                buffer = QtCore.QBuffer(byte_array)
                buffer.open(QtCore.QIODevice.WriteOnly)
                q_image.save(buffer, "JPEG", 50)  # 保存为 jpeg 格式的字节数据
            path = Path(file_path)
            for index in sel_idxes:
                self.query.bindValue(':id', None)
                self.query.bindValue(':mh_id', index.data())
                self.query.bindValue(':name', path.name)
                self.query.bindValue(':image', byte_array)
                if not self.query.exec():
                    self.db.con.rollback()
                    QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
                    return
        self.db.con.commit()
        QtWidgets.QMessageBox.information(self, 'Information', 'Successfully')

    @pyqtSlot()
    def on_btnImageRef_clicked(self):  # TODO
        pass

    @pyqtSlot()
    def on_btnNewPanel_clicked(self):
        panel, _ = QtWidgets.QInputDialog.getText(self, 'Input', 'Panel:')
        if not _:
            return
        proc_id = self.ui.lineEditProcId.text()
        sql = f"""INSERT INTO {self.tb_name_panel} 
                  SELECT:id,:proc_id,:panel
                  WHERE NOT EXISTS (SELECT * FROM {self.tb_name_panel} WHERE proc_id=:proc_id AND panel=:panel)"""
        self.query.prepare(sql)
        self.query.bindValue(":id", None)
        self.query.bindValue(":proc_id", proc_id)
        self.query.bindValue(":panel", panel)
        if not self.query.exec():
            QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
            return
        self.ui.tbvPanel.model().setFilter(f"proc_id='{proc_id}' ORDER BY id,proc_id ASC")
        self.ui.tbvPanel.model().select()

    @pyqtSlot()
    def on_btnDeletePanel_clicked(self):
        proc_id = self.ui.lineEditProcId.text()

        # 执行删除reference程序
        sel_model = self.ui.tbvPanel.selectionModel()
        sel_idxes = sel_model.selectedRows(0)
        sql = f"DELETE FROM {self.tb_name_panel} WHERE id=:id"
        self.query.prepare(sql)
        self.db.con.transaction()
        for x in sel_idxes:
            self.query.bindValue(":id", x.data())
            if not self.query.exec():
                QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
                self.db.con.rollback()
                return
        self.db.con.commit()

        self.ui.tbvPanel.model().setFilter(f"proc_id='{proc_id}' ORDER BY id,proc_id ASC")
        self.ui.tbvPanel.model().select()

    @pyqtSlot()
    def on_btnNewIcw_clicked(self):  # TODO
        proc_id = self.ui.lineEditProcId.text()
        dialog = NewIcwDialog(proc_id)
        dialog.exec()
        self.ui.tbvIcw.model().setFilter(f"proc_id='{proc_id}' ORDER BY id,proc_id ASC")
        self.ui.tbvIcw.model().select()

    @pyqtSlot()
    def on_btnDeleteIcw_clicked(self):  # TODO
        proc_id = self.ui.lineEditProcId.text()

        # 执行删除reference程序
        sel_model = self.ui.tbvIcw.selectionModel()
        sel_idxes = sel_model.selectedRows(0)
        sql = f"DELETE FROM {self.tb_name_icw} WHERE id=:id"
        self.query.prepare(sql)
        self.db.con.transaction()
        for x in sel_idxes:
            self.query.bindValue(":id", x.data())
            if not self.query.exec():
                QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
                self.db.con.rollback()
                return
        self.db.con.commit()

        self.ui.tbvIcw.model().setFilter(f"proc_id='{proc_id}' ORDER BY id,proc_id ASC")
        self.ui.tbvIcw.model().select()

    @pyqtSlot()
    def on_btnNewLabel_clicked(self):
        proc_id = self.ui.lineEditProcId.text()
        dialog = NewProcLabelDialog(proc_id)
        dialog.exec()
        self.ui.tbvLabel.model().setFilter(f"proc_id='{proc_id}' ORDER BY id,proc_id ASC")
        self.ui.tbvLabel.model().select()

    @pyqtSlot()
    def on_btnDeleteLabel_clicked(self):
        proc_id = self.ui.lineEditProcId.text()

        # 执行删除reference程序
        sel_model = self.ui.tbvLabel.selectionModel()
        sel_idxes = sel_model.selectedRows(0)
        sql = f"DELETE FROM {self.tb_name_label} WHERE id=:id"
        self.query.prepare(sql)
        self.db.con.transaction()
        for x in sel_idxes:
            self.query.bindValue(":id", x.data())
            if not self.query.exec():
                QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
                self.db.con.rollback()
                return
        self.db.con.commit()

        self.ui.tbvLabel.model().setFilter(f"proc_id='{proc_id}' ORDER BY id,proc_id ASC")
        self.ui.tbvLabel.model().select()

    @pyqtSlot()
    def on_btnSave_clicked(self):  # TODO
        proc_id = self.ui.lineEditProcId.text()
        desc = self.ui.plainTextEditDesc.toPlainText()
        craft = self.ui.cbbCraftCode.currentText()
        loc = self.ui.cbbLocation.currentText()
        action = self.ui.cbbActionType.currentText()
        access = self.ui.plainTextEditAccessDesc.toPlainText()
        remark = self.ui.plainTextEditRemark.toPlainText()
        if not proc_id or not desc:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Procedure ID and Description empty found!')
            return

        self.db.con.transaction()  # 启动数据库操作事务
        # 保存基本信息
        if self.save_mode == 'NEW':
            sql = f"""INSERT INTO {self.tb_name_proc}
                      VALUES (:proc_id,:craft,:description,:loc,:action,:access,:remark)"""
        else:
            sql = f"""UPDATE {self.tb_name_proc} 
                      SET description=:description,craft_code=:craft,location=:loc,
                            action=:action,access=:access,remark=:remark
                      WHERE proc_id=:proc_id"""
        self.query.prepare(sql)
        self.query.bindValue(':proc_id', proc_id)
        self.query.bindValue(':description', desc)
        self.query.bindValue(':access', access)
        self.query.bindValue(':craft', craft)
        self.query.bindValue(':loc', loc)
        self.query.bindValue(':action', action)
        self.query.bindValue(':remark', remark)
        if not self.query.exec():
            QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
            self.db.con.rollback()
            return

        # 保存图片
        sql = f"""INSERT INTO {self.tb_name_image}
                  VALUES (:id,:proc_id,:name,:image,(SELECT IFNULL(MAX(sheet)+1,1) 
                  FROM {self.tb_name_image} WHERE proc_id=:proc_id))"""
        self.query.prepare(sql)
        for im in self.new_ims:
            with open(im, 'rb') as f:
                image_data = QtCore.QByteArray(f.read())  # 以二进制模式打开图片数据并转化为QByteArray对象
            path = Path(im)
            self.query.bindValue(':id', None)
            self.query.bindValue(':proc_id', proc_id)
            self.query.bindValue(':name', path.name)
            self.query.bindValue(':image', image_data)
            if not self.query.exec():
                self.db.con.rollback()
                QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
                return

        # 提交数据库
        self.db.con.commit()
        QtWidgets.QMessageBox.information(self, 'Information', 'Saved.')
        self.on_btnSearchProc_clicked()

        # 复位编辑相关控件状态
        self.save_mode = 'NEW'
        self.new_ims = []
        self.ui.lineEditProcId.setReadOnly(True)
        self.ui.plainTextEditDesc.setReadOnly(True)
        self.ui.lineEditProcId.setText('')
        self.ui.plainTextEditDesc.setPlainText('')
        self.ui.cbbCraftCode.setCurrentText('')
        self.ui.cbbActionType.setCurrentText('')
        self.ui.cbbLocation.setCurrentText('')
        self.ui.tbvReference.model().setFilter('xxx')
        self.ui.tbvReference.model().select()
        self.ui.tbvPanel.model().setFilter('xxx')
        self.ui.tbvPanel.model().select()
        self.ui.tbvIcw.model().setFilter('xxx')
        self.ui.tbvIcw.model().select()
        self.ui.tbvLabel.model().setFilter('xxx')
        self.ui.tbvLabel.model().select()
        self.set_button_enable(False)

    @pyqtSlot()
    def on_btnAddNewImage_clicked(self):
        file_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Open Image", "",
                                                               "Image Files (*.png *.jpg *.bmp)")
        if not file_paths:
            return
        self.new_ims = file_paths

    def init_proc_table(self):
        table = self.ui.tbvProc
        # 创建表格模型(不可编辑, 默认可排序)
        model = QtSql.QSqlTableModel(self, self.db.con)
        model.setTable(self.tb_name_proc)

        # 创建选择模型
        sel_model = QItemSelectionModel(model)

        # 设置表格数据模型和选择模型
        table.setModel(model)
        table.setSelectionModel(sel_model)

        # 设置表格标题
        self.field_num_proc = self.db.get_field_num(model)  # 获取字段名和序号
        for field, column in self.field_num_proc.items():  # 设置字段显示名
            model.setHeaderData(column, Qt.Horizontal, self.tb_header_proc[field])

        # 设置表格视图属性
        for field, column in self.field_num_proc.items():  # 设置表格列宽度默认行为
            if field in ['description']:
                table.horizontalHeader().setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)
            else:
                table.horizontalHeader().setSectionResizeMode(column, QtWidgets.QHeaderView.ResizeToContents)
            if field not in ['proc_id', 'craft_code', 'description', 'location', 'action']:
                self.ui.tbvProc.hideColumn(column)

        # 设置表格视图的水平标题右击弹出菜单
        table.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        table.horizontalHeader().customContextMenuRequested.connect(self.show_table_header_menu)

        self.on_btnSearchProc_clicked()

    def init_ref_table(self):
        table = self.ui.tbvReference
        table.horizontalHeader().setVisible(False)

        # 创建表格模型(不可编辑, 默认可排序)
        model = QtSql.QSqlTableModel(self, self.db.con)
        model.setTable(self.tb_name_ref)

        # 创建选择模型
        sel_model = QItemSelectionModel(model)

        # 设置表格数据模型和选择模型
        table.setModel(model)
        table.setSelectionModel(sel_model)

        # 设置表格标题
        self.field_num_ref = self.db.get_field_num(model)  # 获取字段名和序号
        for field, column in self.field_num_ref.items():  # 设置字段显示名
            model.setHeaderData(column, Qt.Horizontal, self.tb_header_ref[field])

        # 设置表格视图属性
        for field, column in self.field_num_ref.items():  # 设置表格列宽度默认行为
            if field in ['ref']:
                table.horizontalHeader().setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)
            else:
                table.horizontalHeader().setSectionResizeMode(column, QtWidgets.QHeaderView.ResizeToContents)
            if field not in ['ref']:
                table.hideColumn(column)

    def init_panel_table(self):
        table = self.ui.tbvPanel
        table.horizontalHeader().setVisible(False)
        # 创建表格模型(不可编辑, 默认可排序)
        model = QtSql.QSqlTableModel(self, self.db.con)
        model.setTable(self.tb_name_panel)

        # 创建选择模型
        sel_model = QItemSelectionModel(model)

        # 设置表格数据模型和选择模型
        table.setModel(model)
        table.setSelectionModel(sel_model)

        # 设置表格标题
        self.field_num_panel = self.db.get_field_num(model)  # 获取字段名和序号
        for field, column in self.field_num_panel.items():  # 设置字段显示名
            model.setHeaderData(column, Qt.Horizontal, self.tb_header_panel[field])

        # 设置表格视图属性
        for field, column in self.field_num_panel.items():  # 设置表格列宽度默认行为
            table.horizontalHeader().setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)
            if field in ['id', 'proc_id']:
                table.hideColumn(column)

    def init_icw_table(self):
        table = self.ui.tbvIcw
        table.horizontalHeader().setVisible(False)
        # 创建表格模型(不可编辑, 默认可排序)
        model = QtSql.QSqlTableModel(self, self.db.con)
        model.setTable(self.tb_name_icw)

        # 创建选择模型
        sel_model = QItemSelectionModel(model)

        # 设置表格数据模型和选择模型
        table.setModel(model)
        table.setSelectionModel(sel_model)

        # 设置表格标题
        self.field_num_icw = self.db.get_field_num(model)  # 获取字段名和序号
        for field, column in self.field_num_icw.items():  # 设置字段显示名
            model.setHeaderData(column, Qt.Horizontal, self.tb_header_icw[field])
        # 设置表格视图属性
        for field, column in self.field_num_icw.items():  # 设置表格列宽度默认行为
            if field in ['icw']:
                table.horizontalHeader().setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)
            else:
                table.horizontalHeader().setSectionResizeMode(column, QtWidgets.QHeaderView.ResizeToContents)
            if field in ['id', 'proc_id', 'remark']:
                table.hideColumn(column)

    def init_label_table(self):
        table = self.ui.tbvLabel
        table.horizontalHeader().setVisible(False)
        # 创建表格模型(不可编辑, 默认可排序)
        model = QtSql.QSqlTableModel(self, self.db.con)
        model.setTable(self.tb_name_label)

        # 创建选择模型
        sel_model = QItemSelectionModel(model)

        # 设置表格数据模型和选择模型
        table.setModel(model)
        table.setSelectionModel(sel_model)

        # 设置表格标题
        self.field_num_label = self.db.get_field_num(model)  # 获取字段名和序号
        for field, column in self.field_num_label.items():  # 设置字段显示名
            model.setHeaderData(column, Qt.Horizontal, self.tb_header_label[field])
        # 设置表格视图属性
        for field, column in self.field_num_label.items():  # 设置表格列宽度默认行为
            table.horizontalHeader().setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)
            if field in ['id', 'proc_id', ]:
                table.hideColumn(column)

    def show_table_header_menu(self, pos):
        table = self.ui.tbvProc
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
        column_resizable_action.triggered.connect(lambda: self.set_column_resizable(pos))
        menu.addAction(column_resizable_action)

        # 显示右键菜单
        menu.exec_(table.viewport().mapToGlobal(pos))

    def set_column_resizable(self, pos):
        table = self.ui.tbvProc
        h_header = table.horizontalHeader()
        # 获取右键点击处的列索引
        column = h_header.logicalIndexAt(pos)
        if h_header.sectionResizeMode(column) == QtWidgets.QHeaderView.Interactive:
            h_header.setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)
        else:
            h_header.setSectionResizeMode(column, QtWidgets.QHeaderView.Interactive)

    def set_button_enable(self, enable):
        self.ui.btnNewRef.setEnabled(enable)
        self.ui.btnDeleteRef.setEnabled(enable)
        self.ui.btnAddImageRef.setEnabled(enable)
        self.ui.btnImageRef.setEnabled(enable)
        self.ui.btnNewPanel.setEnabled(enable)
        self.ui.btnDeletePanel.setEnabled(enable)
        self.ui.btnNewIcw.setEnabled(enable)
        self.ui.btnDeleteIcw.setEnabled(enable)
        self.ui.btnAddNewImage.setEnabled(enable)
        self.ui.btnSave.setEnabled(enable)
        self.ui.btnNewLabel.setEnabled(enable)
        self.ui.btnDeleteLabel.setEnabled(enable)

    def set_editor_edited(self, enable):
        self.ui.plainTextEditDesc.setReadOnly(enable)
        self.ui.plainTextEditAccessDesc.setReadOnly(enable)
        self.ui.plainTextEditRemark.setReadOnly(enable)


class NewReferenceDialog(QtWidgets.QDialog):
    def __init__(self, proc_id, parent=None):
        super(NewReferenceDialog, self).__init__(parent)
        self.proc_id = proc_id
        self.db = DatabaseManager()
        self.query = QtSql.QSqlQuery(self.db.con)

        self.ui = Ui_NewReferenceDialog()
        self.ui.setupUi(self)
        self.ui.leProcedure.setText(proc_id)

    def on_buttonBox_accepted(self) -> None:
        ref = self.ui.leReference.text()
        type_ = self.ui.cbbType.currentText()
        if not ref or not type_:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Reference and Type is empty.')
            return

        sql = """INSERT INTO ProcedureRef SELECT :id,:proc_id,:ref,:type
                 WHERE NOT EXISTS (SELECT * FROM ProcedureRef WHERE proc_id=:proc_id AND ref=:ref)"""
        self.query.prepare(sql)
        self.query.bindValue(":id", None)
        self.query.bindValue(":proc_id", self.proc_id)
        self.query.bindValue(":ref", ref)
        self.query.bindValue(":type", type_)
        if not self.query.exec():
            QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())

    def on_buttonBox_rejected(self) -> None:
        pass


class NewIcwDialog(QtWidgets.QDialog):
    def __init__(self, proc_id, id_=None, mode='new', parent=None):
        super(NewIcwDialog, self).__init__(parent)
        self.id_ = id_
        self.proc_id = proc_id
        self.mode = mode
        self.db = DatabaseManager()
        self.query = QtSql.QSqlQuery(self.db.con)

        self.ui = Ui_NewIcwDialog()
        self.ui.setupUi(self)
        self.ui.leProcId.setText(proc_id)

    def on_buttonBox_accepted(self) -> None:
        icw = self.ui.leIcw.text()
        mhr = self.ui.dsbMhr.value()
        remark = self.ui.pltRemark.toPlainText()

        if not icw:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Icw is empty.')
            return
        if self.mode == 'new':
            sql = """INSERT INTO ProcedureIcw VALUES(:id,:proc_id,:icw,:mhr,:remark)"""
        else:
            sql = """UPDATE ProcedureIcw 
                     SET proc_id=:proc_id,icw=:icw,mhr=:mhr,remark=:remark
                     WHERE id=:id"""
        self.query.prepare(sql)
        self.query.bindValue(":id", self.id_)
        self.query.bindValue(":proc_id", self.proc_id)
        self.query.bindValue(":icw", icw)
        self.query.bindValue(":mhr", str(mhr))
        self.query.bindValue(":remark", remark)
        if not self.query.exec():
            QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())

    def on_buttonBox_rejected(self) -> None:
        pass


class NewProcLabelDialog(QtWidgets.QDialog):
    def __init__(self, proc_id, parent=None):
        super(NewProcLabelDialog, self).__init__(parent)
        self.proc_id = proc_id
        self.db = DatabaseManager()
        self.query = QtSql.QSqlQuery(self.db.con)

        self.ui = Ui_NewProcLabelDialog()
        self.ui.setupUi(self)

        items = ['']
        sql = "SELECT label FROM LabelOption WHERE source='procedure' ORDER BY label"
        self.query.exec(sql)
        while self.query.next():
            items.append(self.query.value(0))
        self.ui.comboBox.addItems(items)

    def on_buttonBox_accepted(self) -> None:
        label = self.ui.comboBox.currentText()

        if not label:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Icw is empty.')
            return

        sql = """INSERT INTO ProcedureLabel SELECT :id,:proc_id,:label
                 WHERE NOT EXISTS (SELECT * FROM ProcedureLabel WHERE proc_id=:proc_id AND label=:label)"""
        self.query.prepare(sql)
        self.query.bindValue(":id", None)
        self.query.bindValue(":proc_id", self.proc_id)
        self.query.bindValue(":label", label)
        if not self.query.exec():
            QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())

        sql = """INSERT INTO LabelOption SELECT :id,:label,:source
                 WHERE NOT EXISTS (SELECT * FROM LabelOption WHERE source=:source AND label=:label)"""
        self.query.prepare(sql)
        self.query.bindValue(":id", None)
        self.query.bindValue(":label", label)
        self.query.bindValue(":source", 'procedure')
        if not self.query.exec():
            QtWidgets.QMessageBox.critical(self, 'Error', 'Collect Label failed:\n' + self.query.lastError().text())

    def on_buttonBox_rejected(self) -> None:
        pass
