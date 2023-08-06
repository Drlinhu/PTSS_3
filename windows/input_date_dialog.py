from PyQt5 import QtWidgets, QtCore
from .ui import Ui_DateInputDialog


class DateInputDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DateInputDialog()
        self.ui.setupUi(self)
        self.ui.dateEdit.setDate(QtCore.QDate.currentDate())

    def date(self):
        return self.ui.dateEdit.date().toString('yyyy-MM-dd')

    def set_label(self, label):
        self.ui.label.setText(label)
