import os
from pathlib import Path
import pandas as pd
from PyQt5 import QtWidgets, QtSql
from PyQt5.QtCore import pyqtSlot, Qt, QDateTime, QItemSelectionModel

from ..ui import Ui_MhFinalizedDetailForm
from .nrc_subtask_temp_win import NrcSubtaskTempWin
from utils.database import DatabaseManager


class ManhourFinalizedWin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.query = QtSql.QSqlQuery(self.db.con)

        self.ui = Ui_MhFinalizedDetailForm()
        self.ui.setupUi(self)

    def setData(self, **kw):
        self.ui.lineEditMhId.setText(kw.get('mh_id'))
        self.ui.lineEditClass.setText(kw.get('class'))
        self.ui.lineEditPkgId.setText(kw.get('pkg_id'))
        self.ui.lineEditWo.setText(kw.get('wo'))
        self.ui.lineEditAcType.setText(kw.get('ac_type'))
        self.ui.lineEditRegister.setText(kw.get('register'))
        self.ui.lineEditRefTask.setText(kw.get('ref_task'))
        self.ui.plainTextEditDesc.setPlainText(kw.get('description'))
        self.ui.lineEditTrade.setText(kw.get('trade'))
        self.ui.lineEditAta.setText(kw.get('ata'))
        self.ui.lineEditArea.setText(kw.get('area'))
        self.ui.lineEditZone.setText(kw.get('zone'))
        self.ui.lineEditCategory.setText(kw.get('category'))
        self.ui.lineEditSkill.setText(f"{kw.get('skill'):.2f}")
        self.ui.lineEditUnskill.setText(f"{kw.get('unskill'):.2f}")
        self.ui.lineEditTotal.setText(f"{kw.get('total'):.2f}")
        # self.ui.kw.get('standard')
        self.ui.lineEditDskill.setText(f"{kw.get('dskill'):.2f}")
        self.ui.lineEditDunskill.setText(f"{kw.get('dunskill'):.2f}")
        self.ui.lineEditDtotal.setText(f"{kw.get('dtotal'):.2f}")
        self.ui.plainTextEditRemark.setPlainText(kw.get('remark'))

    @pyqtSlot()
    def on_btnSubtask_clicked(self):  # TODO
        nrc_id = self.ui.lineEditMhId.text()
        self.subtask_win = NrcSubtaskTempWin(nrc_id)
        self.subtask_win.show()

    @pyqtSlot()
    def on_btnImage_clicked(self):  # TODO
        ims = []
        mh_id = self.ui.lineEditMhId.text()

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
