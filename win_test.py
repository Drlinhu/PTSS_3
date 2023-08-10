import sys
from PyQt5.Qt import *
from utils.database import initialize_database
# from windows.manhour import ManhourWin as Win
# from windows.manhour.nrc_report_assistant_win import NrcReportAssistantWin as Win
from windows.progress_bar import ProgressBarDialog as Win

initialize_database()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Win()
    for i in range(101):
        pass
    win.show()
    sys.exit(app.exec_())
