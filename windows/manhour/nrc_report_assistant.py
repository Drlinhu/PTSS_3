from PyQt5.QtWidgets import QWidget

from ..ui import Ui_NrcReprotAssistantForm


class NrcReportAssistantWin(QWidget):
    def __init__(self, parent=None):
        super(NrcReportAssistantWin, self).__init__(parent)
        self.ui = Ui_NrcReprotAssistantForm()
        self.ui.setupUi(self)
