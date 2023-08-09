import os
from pathlib import Path
import pandas as pd
from PyQt5 import QtWidgets, QtSql, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSlot, QDateTime
from utils.database import DatabaseManager

from ..ui import Ui_TextEditDialog


class CxRemarkInputDialog(QtWidgets.QDialog):
    table_header_mapping = {'id': 'Id',
                            'mh_id': 'Mh_Id',
                            'remark': 'Remark',
                            'create_user': 'Create_User',
                            'create_datetime': 'Create_Datetime',
                            'update_user': 'Update_User',
                            'update_datetime': 'Update_Datetime',
                            }

    def __init__(self, parent=None, ignore_text_changed=False, **kw):
        super(CxRemarkInputDialog, self).__init__(parent)
        self.kw = kw
        self.db = DatabaseManager()
        self.query = QtSql.QSqlQuery(self.db.con)
        self.table_name = "MhCxRemark"

        settings = QtCore.QSettings("config.ini", QtCore.QSettings.IniFormat)
        self.current_user = settings.value("current_user/name")
        self.update_date = self.kw.get('update_datetime')
        self.update_user = self.kw.get('update_user')

        self.ui = Ui_TextEditDialog()
        self.ui.setupUi(self)
        self.setWindowTitle('Enter CX Remark')
        self._ignore_text_changed = ignore_text_changed

        if self.kw.get('remark') is not None:
            self.ui.plainTextEdit.setPlainText(self.kw.get('remark'))

    def on_buttonBox_accepted(self):
        fault = False

        remark = self.ui.plainTextEdit.toPlainText()
        if self.kw.get('id_') is None:  # 为新记录
            # 读取.ini文件中的值
            ct_dt = QtCore.QDate.currentDate().toString('yyyy-MM-dd')
            sql = f"INSERT INTO {self.table_name} VALUES(:id,:mh_id,:remark,:ct_user,:ct_dt,:up_user,:up_dt)"
            self.query.prepare(sql)
            self.query.bindValue(':id_', None)
            self.query.bindValue(':mh_id', self.kw.get('mh_id'))
            self.query.bindValue(':remark', remark)
            self.query.bindValue(':ct_user', self.current_user)
            self.query.bindValue(':ct_dt', ct_dt)
            self.query.bindValue(':up_user', self.current_user)
            self.query.bindValue(':up_dt', ct_dt)
            if not self.query.exec():
                fault = True
        else:  # 更新记录
            sql = f"""UPDATE {self.table_name} 
                      SET remark=:remark,update_user=:up_user,update_datetime=:up_dt 
                      WHERE id=:id"""
            self.query.prepare(sql)
            self.query.bindValue(':id', self.kw.get('id_'))
            self.query.bindValue(':remark', remark)
            self.query.bindValue(':up_user', self.update_user)
            self.query.bindValue(':up_dt', self.update_date)
            if not self.query.exec():
                fault = True

        if not fault:
            QtWidgets.QMessageBox.information(self, 'Information', 'Saved successfully!')
        else:
            QtWidgets.QMessageBox.critical(self, 'Error', f'Save Failed\n{self.query.lastError().text()}')

    def on_buttonBox_rejected(self):
        return

    @pyqtSlot()
    def on_plainTextEdit_textChanged(self):
        if not self._ignore_text_changed:  # 初始化时，若本来有内容则不触发
            self.update_date = QtCore.QDate.currentDate().toString('yyyy-MM-dd')
            self.update_user = self.current_user
        self._ignore_text_changed = False  # 初始化后，默认只要改变内容就触发
