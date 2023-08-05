import sys
from PyQt5.Qt import *
from utils.database import initialize_database
# from windows.manhour import ManhourWin as Win
from windows.manhour import NrcReportAssistantWin as Win

initialize_database()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Win()
    win.show()
    sys.exit(app.exec_())
