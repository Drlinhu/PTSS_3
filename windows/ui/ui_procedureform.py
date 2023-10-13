# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'procedureform.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ProcedureForm(object):
    def setupUi(self, ProcedureForm):
        ProcedureForm.setObjectName("ProcedureForm")
        ProcedureForm.resize(1303, 767)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        ProcedureForm.setFont(font)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(ProcedureForm)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtWidgets.QFrame(ProcedureForm)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.tbvProc = QtWidgets.QTableView(self.frame)
        self.tbvProc.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tbvProc.setAlternatingRowColors(True)
        self.tbvProc.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tbvProc.setSortingEnabled(True)
        self.tbvProc.setObjectName("tbvProc")
        self.gridLayout.addWidget(self.tbvProc, 1, 0, 1, 4)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.frame_2.setFont(font)
        self.frame_2.setStyleSheet("#frame_2 {border:1px solid gray}")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnSearchProc = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnSearchProc.setFont(font)
        self.btnSearchProc.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSearchProc.setIcon(icon)
        self.btnSearchProc.setObjectName("btnSearchProc")
        self.verticalLayout.addWidget(self.btnSearchProc)
        self.line = QtWidgets.QFrame(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.line.setFont(font)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.btnImportProc = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnImportProc.setFont(font)
        self.btnImportProc.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/import.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnImportProc.setIcon(icon1)
        self.btnImportProc.setObjectName("btnImportProc")
        self.verticalLayout.addWidget(self.btnImportProc)
        self.btnExportProc = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnExportProc.setFont(font)
        self.btnExportProc.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/export.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnExportProc.setIcon(icon2)
        self.btnExportProc.setObjectName("btnExportProc")
        self.verticalLayout.addWidget(self.btnExportProc)
        self.btnDeleteProc = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnDeleteProc.setFont(font)
        self.btnDeleteProc.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDeleteProc.setIcon(icon3)
        self.btnDeleteProc.setObjectName("btnDeleteProc")
        self.verticalLayout.addWidget(self.btnDeleteProc)
        self.line_2 = QtWidgets.QFrame(self.frame_2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.btnNewProc = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnNewProc.setFont(font)
        self.btnNewProc.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icon/new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnNewProc.setIcon(icon4)
        self.btnNewProc.setObjectName("btnNewProc")
        self.verticalLayout.addWidget(self.btnNewProc)
        self.btnAddImage = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnAddImage.setFont(font)
        self.btnAddImage.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icon/add-image.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAddImage.setIcon(icon5)
        self.btnAddImage.setObjectName("btnAddImage")
        self.verticalLayout.addWidget(self.btnAddImage)
        self.btnImage = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnImage.setFont(font)
        self.btnImage.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icon/image.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnImage.setIcon(icon6)
        self.btnImage.setObjectName("btnImage")
        self.verticalLayout.addWidget(self.btnImage)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addWidget(self.frame_2, 1, 4, 1, 1)
        self.lineEditSearchProcId = QtWidgets.QLineEdit(self.frame)
        self.lineEditSearchProcId.setObjectName("lineEditSearchProcId")
        self.gridLayout.addWidget(self.lineEditSearchProcId, 0, 1, 1, 1)
        self.lineEditSearchDesc = QtWidgets.QLineEdit(self.frame)
        self.lineEditSearchDesc.setObjectName("lineEditSearchDesc")
        self.gridLayout.addWidget(self.lineEditSearchDesc, 0, 3, 1, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(3, 2)
        self.horizontalLayout_2.addWidget(self.frame)
        self.frame_3 = QtWidgets.QFrame(ProcedureForm)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame_8 = QtWidgets.QFrame(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.frame_8.setFont(font)
        self.frame_8.setStyleSheet("#frame_8 {border:1px solid gray}")
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_8)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.btnNewIcw = QtWidgets.QPushButton(self.frame_8)
        self.btnNewIcw.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnNewIcw.setFont(font)
        self.btnNewIcw.setText("")
        self.btnNewIcw.setIcon(icon4)
        self.btnNewIcw.setObjectName("btnNewIcw")
        self.verticalLayout_5.addWidget(self.btnNewIcw)
        self.btnDeleteIcw = QtWidgets.QPushButton(self.frame_8)
        self.btnDeleteIcw.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnDeleteIcw.setFont(font)
        self.btnDeleteIcw.setText("")
        self.btnDeleteIcw.setIcon(icon3)
        self.btnDeleteIcw.setObjectName("btnDeleteIcw")
        self.verticalLayout_5.addWidget(self.btnDeleteIcw)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.gridLayout_2.addWidget(self.frame_8, 7, 2, 1, 1)
        self.plainTextEditDesc = QtWidgets.QPlainTextEdit(self.frame_3)
        self.plainTextEditDesc.setReadOnly(True)
        self.plainTextEditDesc.setObjectName("plainTextEditDesc")
        self.gridLayout_2.addWidget(self.plainTextEditDesc, 1, 1, 1, 1)
        self.plainTextEditRemark = QtWidgets.QPlainTextEdit(self.frame_3)
        self.plainTextEditRemark.setReadOnly(True)
        self.plainTextEditRemark.setObjectName("plainTextEditRemark")
        self.gridLayout_2.addWidget(self.plainTextEditRemark, 9, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame_3)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 6, 0, 1, 1)
        self.frame_5 = QtWidgets.QFrame(self.frame_3)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tbvReference = QtWidgets.QTableView(self.frame_5)
        self.tbvReference.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tbvReference.setAlternatingRowColors(True)
        self.tbvReference.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tbvReference.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tbvReference.setSortingEnabled(True)
        self.tbvReference.setObjectName("tbvReference")
        self.horizontalLayout_3.addWidget(self.tbvReference)
        self.gridLayout_2.addWidget(self.frame_5, 2, 1, 1, 1)
        self.tbvMarker = QtWidgets.QTableView(self.frame_3)
        self.tbvMarker.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tbvMarker.setAlternatingRowColors(True)
        self.tbvMarker.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tbvMarker.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tbvMarker.setSortingEnabled(True)
        self.tbvMarker.setObjectName("tbvMarker")
        self.gridLayout_2.addWidget(self.tbvMarker, 8, 1, 1, 1)
        self.cbbLocation = QtWidgets.QComboBox(self.frame_3)
        self.cbbLocation.setObjectName("cbbLocation")
        self.gridLayout_2.addWidget(self.cbbLocation, 3, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.tbvIcw = QtWidgets.QTableView(self.frame_3)
        self.tbvIcw.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tbvIcw.setAlternatingRowColors(True)
        self.tbvIcw.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tbvIcw.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tbvIcw.setSortingEnabled(True)
        self.tbvIcw.setObjectName("tbvIcw")
        self.gridLayout_2.addWidget(self.tbvIcw, 7, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.frame_3)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 8, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.frame_3)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 7, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.frame_3)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 5, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame_3)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1)
        self.frame_7 = QtWidgets.QFrame(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.frame_7.setFont(font)
        self.frame_7.setStyleSheet("#frame_7 {border:1px solid gray}")
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_7)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.btnNewPanel = QtWidgets.QPushButton(self.frame_7)
        self.btnNewPanel.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnNewPanel.setFont(font)
        self.btnNewPanel.setText("")
        self.btnNewPanel.setIcon(icon4)
        self.btnNewPanel.setObjectName("btnNewPanel")
        self.verticalLayout_4.addWidget(self.btnNewPanel)
        self.btnDeletePanel = QtWidgets.QPushButton(self.frame_7)
        self.btnDeletePanel.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnDeletePanel.setFont(font)
        self.btnDeletePanel.setText("")
        self.btnDeletePanel.setIcon(icon3)
        self.btnDeletePanel.setObjectName("btnDeletePanel")
        self.verticalLayout_4.addWidget(self.btnDeletePanel)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.gridLayout_2.addWidget(self.frame_7, 6, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.frame_3)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 3, 0, 1, 1)
        self.plainTextEditAccessDesc = QtWidgets.QPlainTextEdit(self.frame_3)
        self.plainTextEditAccessDesc.setReadOnly(True)
        self.plainTextEditAccessDesc.setObjectName("plainTextEditAccessDesc")
        self.gridLayout_2.addWidget(self.plainTextEditAccessDesc, 5, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.frame_3)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 9, 0, 1, 1)
        self.frame_10 = QtWidgets.QFrame(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.frame_10.setFont(font)
        self.frame_10.setStyleSheet("#frame_8 {border:1px solid gray}")
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_10)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.btnNewLabel = QtWidgets.QPushButton(self.frame_10)
        self.btnNewLabel.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnNewLabel.setFont(font)
        self.btnNewLabel.setText("")
        self.btnNewLabel.setIcon(icon4)
        self.btnNewLabel.setObjectName("btnNewLabel")
        self.verticalLayout_8.addWidget(self.btnNewLabel)
        self.btnDeleteLabel = QtWidgets.QPushButton(self.frame_10)
        self.btnDeleteLabel.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnDeleteLabel.setFont(font)
        self.btnDeleteLabel.setText("")
        self.btnDeleteLabel.setIcon(icon3)
        self.btnDeleteLabel.setObjectName("btnDeleteLabel")
        self.verticalLayout_8.addWidget(self.btnDeleteLabel)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem3)
        self.gridLayout_2.addWidget(self.frame_10, 8, 2, 1, 1)
        self.lineEditProcId = QtWidgets.QLineEdit(self.frame_3)
        self.lineEditProcId.setReadOnly(True)
        self.lineEditProcId.setObjectName("lineEditProcId")
        self.gridLayout_2.addWidget(self.lineEditProcId, 0, 1, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.frame_3)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tbvPanel = QtWidgets.QTableView(self.frame_4)
        self.tbvPanel.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tbvPanel.setAlternatingRowColors(True)
        self.tbvPanel.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tbvPanel.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tbvPanel.setSortingEnabled(True)
        self.tbvPanel.setObjectName("tbvPanel")
        self.horizontalLayout.addWidget(self.tbvPanel)
        self.gridLayout_2.addWidget(self.frame_4, 6, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame_3)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.frame_6 = QtWidgets.QFrame(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.frame_6.setFont(font)
        self.frame_6.setStyleSheet("#frame_6 {border:1px solid gray}")
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btnNewRef = QtWidgets.QPushButton(self.frame_6)
        self.btnNewRef.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnNewRef.setFont(font)
        self.btnNewRef.setText("")
        self.btnNewRef.setIcon(icon4)
        self.btnNewRef.setObjectName("btnNewRef")
        self.verticalLayout_2.addWidget(self.btnNewRef)
        self.btnDeleteRef = QtWidgets.QPushButton(self.frame_6)
        self.btnDeleteRef.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnDeleteRef.setFont(font)
        self.btnDeleteRef.setText("")
        self.btnDeleteRef.setIcon(icon3)
        self.btnDeleteRef.setObjectName("btnDeleteRef")
        self.verticalLayout_2.addWidget(self.btnDeleteRef)
        self.btnAddImageRef = QtWidgets.QPushButton(self.frame_6)
        self.btnAddImageRef.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnAddImageRef.setFont(font)
        self.btnAddImageRef.setText("")
        self.btnAddImageRef.setIcon(icon5)
        self.btnAddImageRef.setObjectName("btnAddImageRef")
        self.verticalLayout_2.addWidget(self.btnAddImageRef)
        self.btnImageRef = QtWidgets.QPushButton(self.frame_6)
        self.btnImageRef.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnImageRef.setFont(font)
        self.btnImageRef.setText("")
        self.btnImageRef.setIcon(icon6)
        self.btnImageRef.setObjectName("btnImageRef")
        self.verticalLayout_2.addWidget(self.btnImageRef)
        self.gridLayout_2.addWidget(self.frame_6, 2, 2, 1, 1)
        self.frame_9 = QtWidgets.QFrame(self.frame_3)
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_9)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btnAddNewImage = QtWidgets.QPushButton(self.frame_9)
        self.btnAddNewImage.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnAddNewImage.setFont(font)
        self.btnAddNewImage.setText("")
        self.btnAddNewImage.setIcon(icon5)
        self.btnAddNewImage.setObjectName("btnAddNewImage")
        self.horizontalLayout_4.addWidget(self.btnAddNewImage)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.btnSave = QtWidgets.QPushButton(self.frame_9)
        self.btnSave.setEnabled(False)
        self.btnSave.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icon/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSave.setIcon(icon7)
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout_4.addWidget(self.btnSave)
        self.gridLayout_2.addWidget(self.frame_9, 10, 0, 1, 3)
        self.label_12 = QtWidgets.QLabel(self.frame_3)
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 4, 0, 1, 1)
        self.cbbActionType = QtWidgets.QComboBox(self.frame_3)
        self.cbbActionType.setObjectName("cbbActionType")
        self.gridLayout_2.addWidget(self.cbbActionType, 4, 1, 1, 1)
        self.horizontalLayout_2.addWidget(self.frame_3)
        self.toolBox = QtWidgets.QToolBox(ProcedureForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setStyleSheet("")
        self.toolBox.setObjectName("toolBox")
        self.toolBoxPageRef = QtWidgets.QWidget()
        self.toolBoxPageRef.setGeometry(QtCore.QRect(0, 0, 96, 659))
        self.toolBoxPageRef.setObjectName("toolBoxPageRef")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.toolBoxPageRef)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.toolButtonImportRef = QtWidgets.QToolButton(self.toolBoxPageRef)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButtonImportRef.sizePolicy().hasHeightForWidth())
        self.toolButtonImportRef.setSizePolicy(sizePolicy)
        self.toolButtonImportRef.setIcon(icon1)
        self.toolButtonImportRef.setIconSize(QtCore.QSize(20, 20))
        self.toolButtonImportRef.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButtonImportRef.setAutoRaise(True)
        self.toolButtonImportRef.setObjectName("toolButtonImportRef")
        self.verticalLayout_6.addWidget(self.toolButtonImportRef)
        self.toolButtonExportRef = QtWidgets.QToolButton(self.toolBoxPageRef)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButtonExportRef.sizePolicy().hasHeightForWidth())
        self.toolButtonExportRef.setSizePolicy(sizePolicy)
        self.toolButtonExportRef.setIcon(icon2)
        self.toolButtonExportRef.setIconSize(QtCore.QSize(20, 20))
        self.toolButtonExportRef.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButtonExportRef.setAutoRaise(True)
        self.toolButtonExportRef.setObjectName("toolButtonExportRef")
        self.verticalLayout_6.addWidget(self.toolButtonExportRef)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem5)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icon/tool.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolBox.addItem(self.toolBoxPageRef, icon8, "")
        self.toolBoxPagePanel = QtWidgets.QWidget()
        self.toolBoxPagePanel.setGeometry(QtCore.QRect(0, 0, 86, 659))
        self.toolBoxPagePanel.setObjectName("toolBoxPagePanel")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.toolBoxPagePanel)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.toolButtonImportPanel = QtWidgets.QToolButton(self.toolBoxPagePanel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButtonImportPanel.sizePolicy().hasHeightForWidth())
        self.toolButtonImportPanel.setSizePolicy(sizePolicy)
        self.toolButtonImportPanel.setIcon(icon1)
        self.toolButtonImportPanel.setIconSize(QtCore.QSize(20, 20))
        self.toolButtonImportPanel.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButtonImportPanel.setAutoRaise(True)
        self.toolButtonImportPanel.setObjectName("toolButtonImportPanel")
        self.verticalLayout_3.addWidget(self.toolButtonImportPanel)
        self.toolButtonExportPanel = QtWidgets.QToolButton(self.toolBoxPagePanel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButtonExportPanel.sizePolicy().hasHeightForWidth())
        self.toolButtonExportPanel.setSizePolicy(sizePolicy)
        self.toolButtonExportPanel.setIcon(icon2)
        self.toolButtonExportPanel.setIconSize(QtCore.QSize(20, 20))
        self.toolButtonExportPanel.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButtonExportPanel.setAutoRaise(True)
        self.toolButtonExportPanel.setObjectName("toolButtonExportPanel")
        self.verticalLayout_3.addWidget(self.toolButtonExportPanel)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem6)
        self.toolBox.addItem(self.toolBoxPagePanel, icon8, "")
        self.toolBoxPageIcw = QtWidgets.QWidget()
        self.toolBoxPageIcw.setGeometry(QtCore.QRect(0, 0, 96, 659))
        self.toolBoxPageIcw.setObjectName("toolBoxPageIcw")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.toolBoxPageIcw)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.toolButtonImportIcw = QtWidgets.QToolButton(self.toolBoxPageIcw)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButtonImportIcw.sizePolicy().hasHeightForWidth())
        self.toolButtonImportIcw.setSizePolicy(sizePolicy)
        self.toolButtonImportIcw.setIcon(icon1)
        self.toolButtonImportIcw.setIconSize(QtCore.QSize(20, 20))
        self.toolButtonImportIcw.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButtonImportIcw.setAutoRaise(True)
        self.toolButtonImportIcw.setObjectName("toolButtonImportIcw")
        self.verticalLayout_7.addWidget(self.toolButtonImportIcw)
        self.toolButtonExportIcw = QtWidgets.QToolButton(self.toolBoxPageIcw)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButtonExportIcw.sizePolicy().hasHeightForWidth())
        self.toolButtonExportIcw.setSizePolicy(sizePolicy)
        self.toolButtonExportIcw.setIcon(icon2)
        self.toolButtonExportIcw.setIconSize(QtCore.QSize(20, 20))
        self.toolButtonExportIcw.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButtonExportIcw.setAutoRaise(True)
        self.toolButtonExportIcw.setObjectName("toolButtonExportIcw")
        self.verticalLayout_7.addWidget(self.toolButtonExportIcw)
        spacerItem7 = QtWidgets.QSpacerItem(20, 427, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem7)
        self.toolBox.addItem(self.toolBoxPageIcw, icon8, "")
        self.horizontalLayout_2.addWidget(self.toolBox)
        self.horizontalLayout_2.setStretch(0, 1)

        self.retranslateUi(ProcedureForm)
        QtCore.QMetaObject.connectSlotsByName(ProcedureForm)

    def retranslateUi(self, ProcedureForm):
        _translate = QtCore.QCoreApplication.translate
        ProcedureForm.setWindowTitle(_translate("ProcedureForm", "ProcedureForm"))
        self.label.setText(_translate("ProcedureForm", "Procedure ID: "))
        self.label_2.setText(_translate("ProcedureForm", "Description: "))
        self.label_5.setText(_translate("ProcedureForm", "Panel:"))
        self.label_3.setText(_translate("ProcedureForm", "Description:"))
        self.label_10.setText(_translate("ProcedureForm", "Labels:"))
        self.label_7.setText(_translate("ProcedureForm", "ICW:"))
        self.label_8.setText(_translate("ProcedureForm", "Access:"))
        self.label_6.setText(_translate("ProcedureForm", "Reference:"))
        self.label_9.setText(_translate("ProcedureForm", "Location:"))
        self.label_11.setText(_translate("ProcedureForm", "Cx Remark"))
        self.label_4.setText(_translate("ProcedureForm", "Procedure ID:"))
        self.label_12.setText(_translate("ProcedureForm", "Action:"))
        self.toolButtonImportRef.setText(_translate("ProcedureForm", "Import"))
        self.toolButtonExportRef.setText(_translate("ProcedureForm", "Export"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.toolBoxPageRef), _translate("ProcedureForm", "Reference"))
        self.toolButtonImportPanel.setText(_translate("ProcedureForm", "Import"))
        self.toolButtonExportPanel.setText(_translate("ProcedureForm", "Export"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.toolBoxPagePanel), _translate("ProcedureForm", "Panel"))
        self.toolButtonImportIcw.setText(_translate("ProcedureForm", "Import"))
        self.toolButtonExportIcw.setText(_translate("ProcedureForm", "Export"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.toolBoxPageIcw), _translate("ProcedureForm", "ICW"))
import image_rc
