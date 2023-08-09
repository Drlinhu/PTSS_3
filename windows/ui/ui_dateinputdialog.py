# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dateinputdialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DateInputDialog(object):
    def setupUi(self, DateInputDialog):
        DateInputDialog.setObjectName("DateInputDialog")
        DateInputDialog.resize(254, 102)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        DateInputDialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(DateInputDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(DateInputDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.formLayout = QtWidgets.QFormLayout(self.frame)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setHorizontalSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.label_date = QtWidgets.QLabel(self.frame)
        self.label_date.setObjectName("label_date")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_date)
        self.dateEdit = QtWidgets.QDateEdit(self.frame)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName("dateEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.dateEdit)
        self.label_mode = QtWidgets.QLabel(self.frame)
        self.label_mode.setObjectName("label_mode")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_mode)
        self.comboBox = QtWidgets.QComboBox(self.frame)
        self.comboBox.setObjectName("comboBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.verticalLayout.addWidget(self.frame)
        self.buttonBox = QtWidgets.QDialogButtonBox(DateInputDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DateInputDialog)
        self.buttonBox.accepted.connect(DateInputDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(DateInputDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(DateInputDialog)

    def retranslateUi(self, DateInputDialog):
        _translate = QtCore.QCoreApplication.translate
        DateInputDialog.setWindowTitle(_translate("DateInputDialog", "Dialog"))
        self.label_date.setText(_translate("DateInputDialog", "TextLabel:"))
        self.dateEdit.setDisplayFormat(_translate("DateInputDialog", "yyyy-MM-dd"))
        self.label_mode.setText(_translate("DateInputDialog", "Save Model:"))