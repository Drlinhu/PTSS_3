import sys

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import QtGui

from utils.database import *
from .ui import Ui_MainWindow
from windows.manhour.manhour_win import ManhourWin
from windows.procedure.procedure_win import ProcedureWin


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # 设置tabWidget属性
        self.ui.tabWidget.clear()
        self.ui.tabWidget.setVisible(False)
        self.setCentralWidget(self.ui.tabWidget)
        self.setWindowState(Qt.WindowMaximized)  # 窗口最大化显示
        # 初始化数据库
        initialize_database()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        sys.exit()

    @pyqtSlot()
    def on_tabWidget_currentChanged(self, index):  # tabWidget当前页面变化
        hasTabs = self.ui.tabWidget.count() > 0  # 页面个数
        self.ui.tabWidget.setVisible(hasTabs)  # 当页面个数为0时，隐藏tabWidget

    def on_tabWidget_tabCloseRequested(self, index):  # 分页关闭时关闭窗体
        if index < 0:
            return
        aForm = self.ui.tabWidget.widget(index)
        aForm.close()

    @pyqtSlot()
    def on_actionProcedure_triggered(self):
        form = ProcedureWin(self)
        form.setAttribute(Qt.WA_DeleteOnClose)
        curIndex = self.ui.tabWidget.addTab(form, "Procedure")
        self.ui.tabWidget.setCurrentIndex(curIndex)
        self.ui.tabWidget.setVisible(True)

    @pyqtSlot()
    def on_actionManhour_triggered(self):
        form = ManhourWin(self)
        form.setAttribute(Qt.WA_DeleteOnClose)
        curIndex = self.ui.tabWidget.addTab(form, "Manhour")
        self.ui.tabWidget.setCurrentIndex(curIndex)
        self.ui.tabWidget.setVisible(True)

    @pyqtSlot()
    def on_actionPackages_triggered(self):
        pass

    @pyqtSlot()
    def on_actionAircrafts_triggered(self):
        pass
