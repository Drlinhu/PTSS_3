# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'manhourform.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ManHourForm(object):
    def setupUi(self, ManHourForm):
        ManHourForm.setObjectName("ManHourForm")
        ManHourForm.resize(1182, 648)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        ManHourForm.setFont(font)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(ManHourForm)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.frame_10 = QtWidgets.QFrame(ManHourForm)
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.frame_10)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.frame_11 = QtWidgets.QFrame(self.frame_10)
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_11)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frame_14 = QtWidgets.QFrame(self.frame_11)
        self.frame_14.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_14.setObjectName("frame_14")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_14)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.radioButtonNrc = QtWidgets.QRadioButton(self.frame_14)
        self.radioButtonNrc.setChecked(True)
        self.radioButtonNrc.setObjectName("radioButtonNrc")
        self.verticalLayout_7.addWidget(self.radioButtonNrc)
        self.radioButtonRtn = QtWidgets.QRadioButton(self.frame_14)
        self.radioButtonRtn.setChecked(False)
        self.radioButtonRtn.setObjectName("radioButtonRtn")
        self.verticalLayout_7.addWidget(self.radioButtonRtn)
        self.gridLayout_3.addWidget(self.frame_14, 1, 0, 2, 1)
        self.label_13 = QtWidgets.QLabel(self.frame_11)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 2, 2, 1, 1)
        self.doubleSpinBoxSims = QtWidgets.QDoubleSpinBox(self.frame_11)
        self.doubleSpinBoxSims.setEnabled(False)
        self.doubleSpinBoxSims.setMaximum(1.0)
        self.doubleSpinBoxSims.setSingleStep(0.05)
        self.doubleSpinBoxSims.setProperty("value", 0.9)
        self.doubleSpinBoxSims.setObjectName("doubleSpinBoxSims")
        self.gridLayout_3.addWidget(self.doubleSpinBoxSims, 2, 9, 1, 1)
        self.lineEditSearchDesc = QtWidgets.QLineEdit(self.frame_11)
        self.lineEditSearchDesc.setObjectName("lineEditSearchDesc")
        self.gridLayout_3.addWidget(self.lineEditSearchDesc, 2, 3, 1, 3)
        self.lineEditSearchId = QtWidgets.QLineEdit(self.frame_11)
        self.lineEditSearchId.setObjectName("lineEditSearchId")
        self.gridLayout_3.addWidget(self.lineEditSearchId, 1, 3, 1, 1)
        self.frame = QtWidgets.QFrame(self.frame_11)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButtonByWords = QtWidgets.QRadioButton(self.frame)
        self.radioButtonByWords.setChecked(True)
        self.radioButtonByWords.setObjectName("radioButtonByWords")
        self.horizontalLayout.addWidget(self.radioButtonByWords)
        self.radioButtonBySims = QtWidgets.QRadioButton(self.frame)
        self.radioButtonBySims.setObjectName("radioButtonBySims")
        self.horizontalLayout.addWidget(self.radioButtonBySims)
        self.gridLayout_3.addWidget(self.frame, 2, 6, 1, 2)
        self.label_18 = QtWidgets.QLabel(self.frame_11)
        self.label_18.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_18.setObjectName("label_18")
        self.gridLayout_3.addWidget(self.label_18, 2, 8, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.frame_11)
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")
        self.gridLayout_3.addWidget(self.label_17, 1, 6, 1, 1)
        self.lineEditSearchPkgId = QtWidgets.QLineEdit(self.frame_11)
        self.lineEditSearchPkgId.setObjectName("lineEditSearchPkgId")
        self.gridLayout_3.addWidget(self.lineEditSearchPkgId, 1, 9, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.frame_11)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.gridLayout_3.addWidget(self.label_15, 1, 2, 1, 1)
        self.lineEditSearchAcType = QtWidgets.QLineEdit(self.frame_11)
        self.lineEditSearchAcType.setObjectName("lineEditSearchAcType")
        self.gridLayout_3.addWidget(self.lineEditSearchAcType, 1, 5, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.frame_11)
        self.label_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName("label_16")
        self.gridLayout_3.addWidget(self.label_16, 1, 8, 1, 1)
        self.lineEditSearchRegister = QtWidgets.QLineEdit(self.frame_11)
        self.lineEditSearchRegister.setObjectName("lineEditSearchRegister")
        self.gridLayout_3.addWidget(self.lineEditSearchRegister, 1, 7, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.frame_11)
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 1, 4, 1, 1)
        self.line = QtWidgets.QFrame(self.frame_11)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_3.addWidget(self.line, 1, 1, 2, 1)
        self.verticalLayout_11.addWidget(self.frame_11)
        self.frame_12 = QtWidgets.QFrame(self.frame_10)
        self.frame_12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_12")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_12)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.tableViewNrc_2 = QtWidgets.QTableView(self.frame_12)
        self.tableViewNrc_2.setObjectName("tableViewNrc_2")
        self.horizontalLayout_10.addWidget(self.tableViewNrc_2)
        self.frame_13 = QtWidgets.QFrame(self.frame_12)
        self.frame_13.setStyleSheet(" #frame_13 {border:1px solid gray}")
        self.frame_13.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_13.setObjectName("frame_13")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_13)
        self.verticalLayout_8.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_8.setSpacing(6)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.pushButtonSearch = QtWidgets.QPushButton(self.frame_13)
        self.pushButtonSearch.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonSearch.setIcon(icon)
        self.pushButtonSearch.setObjectName("pushButtonSearch")
        self.verticalLayout_8.addWidget(self.pushButtonSearch)
        self.pushButtonExport = QtWidgets.QPushButton(self.frame_13)
        self.pushButtonExport.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/export.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonExport.setIcon(icon1)
        self.pushButtonExport.setObjectName("pushButtonExport")
        self.verticalLayout_8.addWidget(self.pushButtonExport)
        self.pushButtonDelete = QtWidgets.QPushButton(self.frame_13)
        self.pushButtonDelete.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonDelete.setIcon(icon2)
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.verticalLayout_8.addWidget(self.pushButtonDelete)
        self.pushButtonSubtask = QtWidgets.QPushButton(self.frame_13)
        self.pushButtonSubtask.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/subtask.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonSubtask.setIcon(icon3)
        self.pushButtonSubtask.setObjectName("pushButtonSubtask")
        self.verticalLayout_8.addWidget(self.pushButtonSubtask)
        self.pushButtonAddImage = QtWidgets.QPushButton(self.frame_13)
        self.pushButtonAddImage.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icon/add-image.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonAddImage.setIcon(icon4)
        self.pushButtonAddImage.setObjectName("pushButtonAddImage")
        self.verticalLayout_8.addWidget(self.pushButtonAddImage)
        self.pushButtonImage = QtWidgets.QPushButton(self.frame_13)
        self.pushButtonImage.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icon/image.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonImage.setIcon(icon5)
        self.pushButtonImage.setObjectName("pushButtonImage")
        self.verticalLayout_8.addWidget(self.pushButtonImage)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem)
        self.horizontalLayout_10.addWidget(self.frame_13)
        self.verticalLayout_11.addWidget(self.frame_12)
        self.horizontalLayout_9.addWidget(self.frame_10)
        self.frame_15 = QtWidgets.QFrame(ManHourForm)
        self.frame_15.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_15.setObjectName("frame_15")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_15)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.toolBox = QtWidgets.QToolBox(self.frame_15)
        self.toolBox.setObjectName("toolBox")
        self.ToolBoxNrc = QtWidgets.QWidget()
        self.ToolBoxNrc.setGeometry(QtCore.QRect(0, 0, 161, 570))
        self.ToolBoxNrc.setObjectName("ToolBoxNrc")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.ToolBoxNrc)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.toolButtonNrcReportAssistant = QtWidgets.QToolButton(self.ToolBoxNrc)
        self.toolButtonNrcReportAssistant.setToolTip("NRC Report Assistant")
        self.toolButtonNrcReportAssistant.setToolTipDuration(-1)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icon/daily-report.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonNrcReportAssistant.setIcon(icon6)
        self.toolButtonNrcReportAssistant.setIconSize(QtCore.QSize(28, 28))
        self.toolButtonNrcReportAssistant.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButtonNrcReportAssistant.setAutoRaise(True)
        self.toolButtonNrcReportAssistant.setArrowType(QtCore.Qt.NoArrow)
        self.toolButtonNrcReportAssistant.setObjectName("toolButtonNrcReportAssistant")
        self.verticalLayout_12.addWidget(self.toolButtonNrcReportAssistant)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_12.addItem(spacerItem1)
        self.toolBox.addItem(self.ToolBoxNrc, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 161, 570))
        self.page_2.setObjectName("page_2")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.toolButtonRtnReportAssistant = QtWidgets.QToolButton(self.page_2)
        self.toolButtonRtnReportAssistant.setToolTip("NRC Report Assistant")
        self.toolButtonRtnReportAssistant.setToolTipDuration(-1)
        self.toolButtonRtnReportAssistant.setIcon(icon6)
        self.toolButtonRtnReportAssistant.setIconSize(QtCore.QSize(28, 28))
        self.toolButtonRtnReportAssistant.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButtonRtnReportAssistant.setAutoRaise(True)
        self.toolButtonRtnReportAssistant.setArrowType(QtCore.Qt.NoArrow)
        self.toolButtonRtnReportAssistant.setObjectName("toolButtonRtnReportAssistant")
        self.verticalLayout_13.addWidget(self.toolButtonRtnReportAssistant)
        spacerItem2 = QtWidgets.QSpacerItem(20, 508, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_13.addItem(spacerItem2)
        self.toolBox.addItem(self.page_2, "")
        self.verticalLayout_10.addWidget(self.toolBox)
        self.horizontalLayout_9.addWidget(self.frame_15)
        self.horizontalLayout_9.setStretch(0, 1)

        self.retranslateUi(ManHourForm)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ManHourForm)

    def retranslateUi(self, ManHourForm):
        _translate = QtCore.QCoreApplication.translate
        ManHourForm.setWindowTitle(_translate("ManHourForm", "Form"))
        self.radioButtonNrc.setText(_translate("ManHourForm", "NRC"))
        self.radioButtonRtn.setText(_translate("ManHourForm", "RTN"))
        self.label_13.setText(_translate("ManHourForm", "Desc:"))
        self.radioButtonByWords.setText(_translate("ManHourForm", "By Words"))
        self.radioButtonBySims.setText(_translate("ManHourForm", "By Sims"))
        self.label_18.setText(_translate("ManHourForm", "Similarity:"))
        self.label_17.setText(_translate("ManHourForm", "Register:"))
        self.label_15.setText(_translate("ManHourForm", "ID:"))
        self.label_16.setText(_translate("ManHourForm", "Package ID:"))
        self.label_14.setText(_translate("ManHourForm", "AC Type:"))
        self.pushButtonExport.setToolTip(_translate("ManHourForm", "Expprt table data"))
        self.pushButtonSubtask.setToolTip(_translate("ManHourForm", "Open subtasks"))
        self.pushButtonAddImage.setToolTip(_translate("ManHourForm", "Add image"))
        self.pushButtonImage.setToolTip(_translate("ManHourForm", "Open iamge"))
        self.toolButtonNrcReportAssistant.setText(_translate("ManHourForm", "Report Assistant"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.ToolBoxNrc), _translate("ManHourForm", "NRC"))
        self.toolButtonRtnReportAssistant.setText(_translate("ManHourForm", "Report Assistant"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("ManHourForm", "RTN"))
import image_rc
