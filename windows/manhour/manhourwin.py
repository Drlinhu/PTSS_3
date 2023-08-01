from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot

from ..ui.ui_manhourform import Ui_ManHourForm
from .nrc_report_assistant import NrcReportAssistantWin


class ManhourWin(QWidget):
    def __init__(self, parent=None):
        super(ManhourWin, self).__init__()
        self.ui = Ui_ManHourForm()
        self.ui.setupUi(self)

    @pyqtSlot()
    def on_toolButtonNrcReportAssistant_clicked(self):
        self.nrc_reportAssistant_win = NrcReportAssistantWin()
        self.nrc_reportAssistant_win.show()
