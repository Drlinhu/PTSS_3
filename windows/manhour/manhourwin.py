from PyQt5.QtWidgets import QWidget

from ..ui.ui_manhourform import Ui_ManHourForm


class ManhourWin(QWidget):
    def __init__(self, parent=None):
        super(ManhourWin, self).__init__()
        self.ui = Ui_ManHourForm()
        self.ui.setupUi(self)
