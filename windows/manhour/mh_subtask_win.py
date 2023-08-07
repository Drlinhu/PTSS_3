import os
from pathlib import Path
import pandas as pd
from PyQt5 import QtWidgets, QtSql, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSlot, QDateTime

from ..ui import Ui_MhSubtaskForm
from utils.database import DatabaseManager
from utils.corpus import *

__all__ = ['TABLE_HEADER_MAPPING', 'MhSubtaskWin']

TABLE_HEADER_MAPPING = {'register': 'Register',
                        'proj_id': 'Proj_Id',
                        'class': 'Class',
                        'sheet': 'Sheet',
                        'item_no': 'Item_No',
                        'description': 'Description',
                        'jsn': 'Jsn',
                        'mhr': 'Mhr',
                        'trade': 'Trade',
                        }


class MhSubtaskWin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MhSubtaskWin, self).__init__(parent)
        self.ui = Ui_MhSubtaskForm()
        self.ui.setupUi(self)

        self.table_name = "MhSubtask"
        self.db = DatabaseManager()
        self.query = QtSql.QSqlQuery(self.db.con)

        self.init_table()

    def init_table(self):
        pass
