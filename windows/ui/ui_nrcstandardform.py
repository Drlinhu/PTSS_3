# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nrcstandardform.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NrcStandardForm(object):
    def setupUi(self, NrcStandardForm):
        NrcStandardForm.setObjectName("NrcStandardForm")
        NrcStandardForm.resize(1131, 474)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        NrcStandardForm.setFont(font)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(NrcStandardForm)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.frame_3 = QtWidgets.QFrame(NrcStandardForm)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.frame_3.setFont(font)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_2 = QtWidgets.QFrame(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.frame_2.setFont(font)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_16 = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout.addWidget(self.label_16)
        self.cbbSearchAcType = QtWidgets.QComboBox(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.cbbSearchAcType.setFont(font)
        self.cbbSearchAcType.setObjectName("cbbSearchAcType")
        self.cbbSearchAcType.addItem("")
        self.cbbSearchAcType.setItemText(0, "")
        self.cbbSearchAcType.addItem("")
        self.cbbSearchAcType.addItem("")
        self.cbbSearchAcType.addItem("")
        self.horizontalLayout.addWidget(self.cbbSearchAcType)
        self.label = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEditSearchDesc = QtWidgets.QLineEdit(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lineEditSearchDesc.setFont(font)
        self.lineEditSearchDesc.setObjectName("lineEditSearchDesc")
        self.horizontalLayout.addWidget(self.lineEditSearchDesc)
        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.frame_4.setFont(font)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tbvNrcItem = QtWidgets.QTableView(self.frame_4)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.tbvNrcItem.setFont(font)
        self.tbvNrcItem.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tbvNrcItem.setAlternatingRowColors(True)
        self.tbvNrcItem.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tbvNrcItem.setSortingEnabled(True)
        self.tbvNrcItem.setObjectName("tbvNrcItem")
        self.horizontalLayout_2.addWidget(self.tbvNrcItem)
        self.gridLayout.addWidget(self.frame_4, 1, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.frame.setFont(font)
        self.frame.setStyleSheet("#frame {border:1px solid gray}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnSearch = QtWidgets.QPushButton(self.frame)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnSearch.setFont(font)
        self.btnSearch.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSearch.setIcon(icon)
        self.btnSearch.setObjectName("btnSearch")
        self.verticalLayout.addWidget(self.btnSearch)
        self.line = QtWidgets.QFrame(self.frame)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.line.setFont(font)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.btnImport = QtWidgets.QPushButton(self.frame)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnImport.setFont(font)
        self.btnImport.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/import.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnImport.setIcon(icon1)
        self.btnImport.setObjectName("btnImport")
        self.verticalLayout.addWidget(self.btnImport)
        self.btnExport = QtWidgets.QPushButton(self.frame)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnExport.setFont(font)
        self.btnExport.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/export.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnExport.setIcon(icon2)
        self.btnExport.setObjectName("btnExport")
        self.verticalLayout.addWidget(self.btnExport)
        self.btnDelete = QtWidgets.QPushButton(self.frame)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnDelete.setFont(font)
        self.btnDelete.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDelete.setIcon(icon3)
        self.btnDelete.setObjectName("btnDelete")
        self.verticalLayout.addWidget(self.btnDelete)
        self.line_2 = QtWidgets.QFrame(self.frame)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.btnNew = QtWidgets.QPushButton(self.frame)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnNew.setFont(font)
        self.btnNew.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icon/new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnNew.setIcon(icon4)
        self.btnNew.setObjectName("btnNew")
        self.verticalLayout.addWidget(self.btnNew)
        self.btnAddImage = QtWidgets.QPushButton(self.frame)
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
        self.btnImage = QtWidgets.QPushButton(self.frame)
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
        self.gridLayout.addWidget(self.frame, 1, 1, 1, 1)
        self.horizontalLayout_5.addWidget(self.frame_3)
        self.frame_7 = QtWidgets.QFrame(NrcStandardForm)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.frame_7.setFont(font)
        self.frame_7.setStyleSheet("")
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_7)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_6 = QtWidgets.QFrame(self.frame_7)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.frame_6.setFont(font)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_6)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lineEditIemNo = QtWidgets.QLineEdit(self.frame_6)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lineEditIemNo.setFont(font)
        self.lineEditIemNo.setText("")
        self.lineEditIemNo.setReadOnly(True)
        self.lineEditIemNo.setObjectName("lineEditIemNo")
        self.gridLayout_3.addWidget(self.lineEditIemNo, 0, 1, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.frame_6)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.gridLayout_3.addWidget(self.label_18, 0, 2, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.frame_6)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.gridLayout_3.addWidget(self.label_17, 0, 4, 1, 1)
        self.lineEditDesc = QtWidgets.QLineEdit(self.frame_6)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lineEditDesc.setFont(font)
        self.lineEditDesc.setObjectName("lineEditDesc")
        self.gridLayout_3.addWidget(self.lineEditDesc, 2, 1, 1, 5)
        self.label_13 = QtWidgets.QLabel(self.frame_6)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 2, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.frame_6)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.gridLayout_3.addWidget(self.label_15, 0, 0, 1, 1)
        self.cbbWorkArea = QtWidgets.QComboBox(self.frame_6)
        self.cbbWorkArea.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.cbbWorkArea.setFont(font)
        self.cbbWorkArea.setEditable(False)
        self.cbbWorkArea.setObjectName("cbbWorkArea")
        self.cbbWorkArea.addItem("")
        self.cbbWorkArea.setItemText(0, "")
        self.cbbWorkArea.addItem("")
        self.cbbWorkArea.addItem("")
        self.cbbWorkArea.addItem("")
        self.cbbWorkArea.addItem("")
        self.cbbWorkArea.addItem("")
        self.cbbWorkArea.addItem("")
        self.cbbWorkArea.addItem("")
        self.cbbWorkArea.addItem("")
        self.gridLayout_3.addWidget(self.cbbWorkArea, 0, 5, 1, 1)
        self.cbbAcType = QtWidgets.QComboBox(self.frame_6)
        self.cbbAcType.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.cbbAcType.setFont(font)
        self.cbbAcType.setObjectName("cbbAcType")
        self.cbbAcType.addItem("")
        self.cbbAcType.setItemText(0, "")
        self.cbbAcType.addItem("")
        self.cbbAcType.addItem("")
        self.cbbAcType.addItem("")
        self.gridLayout_3.addWidget(self.cbbAcType, 0, 3, 1, 1)
        self.gridLayout_3.setColumnStretch(3, 1)
        self.gridLayout_3.setColumnStretch(5, 1)
        self.verticalLayout_2.addWidget(self.frame_6)
        self.frame_5 = QtWidgets.QFrame(self.frame_7)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.frame_5.setFont(font)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_5)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 2, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 8, 0, 1, 1)
        self.doubleSpinBoxAIMax = QtWidgets.QDoubleSpinBox(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.doubleSpinBoxAIMax.setFont(font)
        self.doubleSpinBoxAIMax.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxAIMax.setReadOnly(True)
        self.doubleSpinBoxAIMax.setMaximum(100000.0)
        self.doubleSpinBoxAIMax.setSingleStep(0.5)
        self.doubleSpinBoxAIMax.setObjectName("doubleSpinBoxAIMax")
        self.gridLayout_2.addWidget(self.doubleSpinBoxAIMax, 1, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 10, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 1, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 3, 0, 1, 1)
        self.doubleSpinBoxAEMin = QtWidgets.QDoubleSpinBox(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.doubleSpinBoxAEMin.setFont(font)
        self.doubleSpinBoxAEMin.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxAEMin.setReadOnly(True)
        self.doubleSpinBoxAEMin.setMaximum(100000.0)
        self.doubleSpinBoxAEMin.setSingleStep(0.5)
        self.doubleSpinBoxAEMin.setObjectName("doubleSpinBoxAEMin")
        self.gridLayout_2.addWidget(self.doubleSpinBoxAEMin, 3, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 4, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 7, 0, 1, 1)
        self.doubleSpinBoxAIMin = QtWidgets.QDoubleSpinBox(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.doubleSpinBoxAIMin.setFont(font)
        self.doubleSpinBoxAIMin.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxAIMin.setReadOnly(True)
        self.doubleSpinBoxAIMin.setMaximum(100000.0)
        self.doubleSpinBoxAIMin.setSingleStep(0.5)
        self.doubleSpinBoxAIMin.setObjectName("doubleSpinBoxAIMin")
        self.gridLayout_2.addWidget(self.doubleSpinBoxAIMin, 1, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 6, 0, 1, 1)
        self.plainTextEditRemark = QtWidgets.QPlainTextEdit(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.plainTextEditRemark.setFont(font)
        self.plainTextEditRemark.setReadOnly(True)
        self.plainTextEditRemark.setObjectName("plainTextEditRemark")
        self.gridLayout_2.addWidget(self.plainTextEditRemark, 1, 3, 10, 1)
        self.label_8 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 5, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 9, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.gridLayout_2.addWidget(self.label_14, 0, 3, 1, 1)
        self.doubleSpinBoxAEMax = QtWidgets.QDoubleSpinBox(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.doubleSpinBoxAEMax.setFont(font)
        self.doubleSpinBoxAEMax.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxAEMax.setReadOnly(True)
        self.doubleSpinBoxAEMax.setMaximum(100000.0)
        self.doubleSpinBoxAEMax.setSingleStep(0.5)
        self.doubleSpinBoxAEMax.setObjectName("doubleSpinBoxAEMax")
        self.gridLayout_2.addWidget(self.doubleSpinBoxAEMax, 3, 2, 1, 1)
        self.doubleSpinBoxAVMin = QtWidgets.QDoubleSpinBox(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.doubleSpinBoxAVMin.setFont(font)
        self.doubleSpinBoxAVMin.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxAVMin.setReadOnly(True)
        self.doubleSpinBoxAVMin.setMaximum(100000.0)
        self.doubleSpinBoxAVMin.setSingleStep(0.5)
        self.doubleSpinBoxAVMin.setObjectName("doubleSpinBoxAVMin")
        self.gridLayout_2.addWidget(self.doubleSpinBoxAVMin, 4, 1, 1, 1)
        self.doubleSpinBoxAVMax = QtWidgets.QDoubleSpinBox(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.doubleSpinBoxAVMax.setFont(font)
        self.doubleSpinBoxAVMax.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxAVMax.setReadOnly(True)
        self.doubleSpinBoxAVMax.setMaximum(100000.0)
        self.doubleSpinBoxAVMax.setSingleStep(0.5)
        self.doubleSpinBoxAVMax.setObjectName("doubleSpinBoxAVMax")
        self.gridLayout_2.addWidget(self.doubleSpinBoxAVMax, 4, 2, 1, 1)
        self.doubleSpinBoxSSMin = QtWidgets.QDoubleSpinBox(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.doubleSpinBoxSSMin.setFont(font)
        self.doubleSpinBoxSSMin.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxSSMin.setReadOnly(True)
        self.doubleSpinBoxSSMin.setMaximum(100000.0)
        self.doubleSpinBoxSSMin.setSingleStep(0.5)
        self.doubleSpinBoxSSMin.setObjectName("doubleSpinBoxSSMin")
        self.gridLayout_2.addWidget(self.doubleSpinBoxSSMin, 5, 1, 1, 1)
        self.doubleSpinBoxSSMax = QtWidgets.QDoubleSpinBox(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.doubleSpinBoxSSMax.setFont(font)
        self.doubleSpinBoxSSMax.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxSSMax.setReadOnly(True)
        self.doubleSpinBoxSSMax.setMaximum(100000.0)
        self.doubleSpinBoxSSMax.setSingleStep(0.5)
        self.doubleSpinBoxSSMax.setObjectName("doubleSpinBoxSSMax")
        self.gridLayout_2.addWidget(self.doubleSpinBoxSSMax, 5, 2, 1, 1)
        self.doubleSpinBoxPTMin = QtWidgets.QDoubleSpinBox(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.doubleSpinBoxPTMin.setFont(font)
        self.doubleSpinBoxPTMin.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxPTMin.setReadOnly(True)
        self.doubleSpinBoxPTMin.setMaximum(100000.0)
        self.doubleSpinBoxPTMin.setSingleStep(0.5)
        self.doubleSpinBoxPTMin.setObjectName("doubleSpinBoxPTMin")
        self.gridLayout_2.addWidget(self.doubleSpinBoxPTMin, 6, 1, 1, 1)
        self.doubleSpinBoxPTMax = QtWidgets.QDoubleSpinBox(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.doubleSpinBoxPTMax.setFont(font)
        self.doubleSpinBoxPTMax.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxPTMax.setReadOnly(True)
        self.doubleSpinBoxPTMax.setMaximum(100000.0)
        self.doubleSpinBoxPTMax.setSingleStep(0.5)
        self.doubleSpinBoxPTMax.setObjectName("doubleSpinBoxPTMax")
        self.gridLayout_2.addWidget(self.doubleSpinBoxPTMax, 6, 2, 1, 1)
        self.doubleSpinBoxSMMin = QtWidgets.QDoubleSpinBox(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.doubleSpinBoxSMMin.setFont(font)
        self.doubleSpinBoxSMMin.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxSMMin.setReadOnly(True)
        self.doubleSpinBoxSMMin.setMaximum(100000.0)
        self.doubleSpinBoxSMMin.setSingleStep(0.5)
        self.doubleSpinBoxSMMin.setObjectName("doubleSpinBoxSMMin")
        self.gridLayout_2.addWidget(self.doubleSpinBoxSMMin, 7, 1, 1, 1)
        self.doubleSpinBoxSMMax = QtWidgets.QDoubleSpinBox(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.doubleSpinBoxSMMax.setFont(font)
        self.doubleSpinBoxSMMax.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxSMMax.setReadOnly(True)
        self.doubleSpinBoxSMMax.setMaximum(100000.0)
        self.doubleSpinBoxSMMax.setSingleStep(0.5)
        self.doubleSpinBoxSMMax.setObjectName("doubleSpinBoxSMMax")
        self.gridLayout_2.addWidget(self.doubleSpinBoxSMMax, 7, 2, 1, 1)
        self.doubleSpinBoxGWMin = QtWidgets.QDoubleSpinBox(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.doubleSpinBoxGWMin.setFont(font)
        self.doubleSpinBoxGWMin.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxGWMin.setReadOnly(True)
        self.doubleSpinBoxGWMin.setMaximum(100000.0)
        self.doubleSpinBoxGWMin.setSingleStep(0.5)
        self.doubleSpinBoxGWMin.setObjectName("doubleSpinBoxGWMin")
        self.gridLayout_2.addWidget(self.doubleSpinBoxGWMin, 8, 1, 1, 1)
        self.doubleSpinBoxGWMax = QtWidgets.QDoubleSpinBox(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.doubleSpinBoxGWMax.setFont(font)
        self.doubleSpinBoxGWMax.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxGWMax.setReadOnly(True)
        self.doubleSpinBoxGWMax.setMaximum(100000.0)
        self.doubleSpinBoxGWMax.setSingleStep(0.5)
        self.doubleSpinBoxGWMax.setObjectName("doubleSpinBoxGWMax")
        self.gridLayout_2.addWidget(self.doubleSpinBoxGWMax, 8, 2, 1, 1)
        self.doubleSpinBoxCLMin = QtWidgets.QDoubleSpinBox(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.doubleSpinBoxCLMin.setFont(font)
        self.doubleSpinBoxCLMin.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxCLMin.setReadOnly(True)
        self.doubleSpinBoxCLMin.setMaximum(100000.0)
        self.doubleSpinBoxCLMin.setSingleStep(0.5)
        self.doubleSpinBoxCLMin.setObjectName("doubleSpinBoxCLMin")
        self.gridLayout_2.addWidget(self.doubleSpinBoxCLMin, 9, 1, 1, 1)
        self.doubleSpinBoxCLMax = QtWidgets.QDoubleSpinBox(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.doubleSpinBoxCLMax.setFont(font)
        self.doubleSpinBoxCLMax.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxCLMax.setReadOnly(True)
        self.doubleSpinBoxCLMax.setMaximum(100000.0)
        self.doubleSpinBoxCLMax.setSingleStep(0.5)
        self.doubleSpinBoxCLMax.setObjectName("doubleSpinBoxCLMax")
        self.gridLayout_2.addWidget(self.doubleSpinBoxCLMax, 9, 2, 1, 1)
        self.doubleSpinBoxTotalMin = QtWidgets.QDoubleSpinBox(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.doubleSpinBoxTotalMin.setFont(font)
        self.doubleSpinBoxTotalMin.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxTotalMin.setReadOnly(True)
        self.doubleSpinBoxTotalMin.setMaximum(100000.0)
        self.doubleSpinBoxTotalMin.setSingleStep(0.5)
        self.doubleSpinBoxTotalMin.setObjectName("doubleSpinBoxTotalMin")
        self.gridLayout_2.addWidget(self.doubleSpinBoxTotalMin, 10, 1, 1, 1)
        self.doubleSpinBoxTotalMax = QtWidgets.QDoubleSpinBox(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.doubleSpinBoxTotalMax.setFont(font)
        self.doubleSpinBoxTotalMax.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxTotalMax.setReadOnly(True)
        self.doubleSpinBoxTotalMax.setMaximum(100000.0)
        self.doubleSpinBoxTotalMax.setSingleStep(0.5)
        self.doubleSpinBoxTotalMax.setObjectName("doubleSpinBoxTotalMax")
        self.gridLayout_2.addWidget(self.doubleSpinBoxTotalMax, 10, 2, 1, 1)
        self.verticalLayout_2.addWidget(self.frame_5)
        self.frame_8 = QtWidgets.QFrame(self.frame_7)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.frame_8.setFont(font)
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btnNewImage = QtWidgets.QPushButton(self.frame_8)
        self.btnNewImage.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnNewImage.setFont(font)
        self.btnNewImage.setText("")
        self.btnNewImage.setIcon(icon5)
        self.btnNewImage.setObjectName("btnNewImage")
        self.horizontalLayout_4.addWidget(self.btnNewImage)
        spacerItem1 = QtWidgets.QSpacerItem(549, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.btnSave = QtWidgets.QPushButton(self.frame_8)
        self.btnSave.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnSave.setFont(font)
        self.btnSave.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icon/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSave.setIcon(icon7)
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout_4.addWidget(self.btnSave)
        self.verticalLayout_2.addWidget(self.frame_8)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.horizontalLayout_5.addWidget(self.frame_7)
        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 1)

        self.retranslateUi(NrcStandardForm)
        self.cbbSearchAcType.setCurrentIndex(3)
        self.cbbWorkArea.setCurrentIndex(0)
        self.cbbAcType.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(NrcStandardForm)

    def retranslateUi(self, NrcStandardForm):
        _translate = QtCore.QCoreApplication.translate
        NrcStandardForm.setWindowTitle(_translate("NrcStandardForm", "NRC Standard Item"))
        self.label_16.setText(_translate("NrcStandardForm", "AC Type: "))
        self.cbbSearchAcType.setItemText(1, _translate("NrcStandardForm", "A330"))
        self.cbbSearchAcType.setItemText(2, _translate("NrcStandardForm", "A350"))
        self.cbbSearchAcType.setItemText(3, _translate("NrcStandardForm", "B777"))
        self.label.setText(_translate("NrcStandardForm", "Desc."))
        self.label_18.setText(_translate("NrcStandardForm", "AC Type: "))
        self.label_17.setText(_translate("NrcStandardForm", "Work Area: "))
        self.label_13.setText(_translate("NrcStandardForm", "Desc."))
        self.label_15.setText(_translate("NrcStandardForm", "Item No:"))
        self.cbbWorkArea.setItemText(1, _translate("NrcStandardForm", "CAB"))
        self.cbbWorkArea.setItemText(2, _translate("NrcStandardForm", "EMP"))
        self.cbbWorkArea.setItemText(3, _translate("NrcStandardForm", "ENG"))
        self.cbbWorkArea.setItemText(4, _translate("NrcStandardForm", "F/T"))
        self.cbbWorkArea.setItemText(5, _translate("NrcStandardForm", "FUS"))
        self.cbbWorkArea.setItemText(6, _translate("NrcStandardForm", "LDG"))
        self.cbbWorkArea.setItemText(7, _translate("NrcStandardForm", "LWR"))
        self.cbbWorkArea.setItemText(8, _translate("NrcStandardForm", "WNG"))
        self.cbbAcType.setItemText(1, _translate("NrcStandardForm", "A330"))
        self.cbbAcType.setItemText(2, _translate("NrcStandardForm", "A350"))
        self.cbbAcType.setItemText(3, _translate("NrcStandardForm", "B777"))
        self.label_3.setText(_translate("NrcStandardForm", "Min"))
        self.label_4.setText(_translate("NrcStandardForm", "Max"))
        self.label_12.setText(_translate("NrcStandardForm", "GW:"))
        self.label_5.setText(_translate("NrcStandardForm", "Total:"))
        self.label_6.setText(_translate("NrcStandardForm", "AI:"))
        self.label_7.setText(_translate("NrcStandardForm", "AE:"))
        self.label_11.setText(_translate("NrcStandardForm", "AV"))
        self.label_10.setText(_translate("NrcStandardForm", "SM:"))
        self.label_9.setText(_translate("NrcStandardForm", "PT:"))
        self.label_8.setText(_translate("NrcStandardForm", "SS:"))
        self.label_2.setText(_translate("NrcStandardForm", "CL:"))
        self.label_14.setText(_translate("NrcStandardForm", "Remark"))
import image_rc
