# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'generalinputdialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GeneralInputDialog(object):
    def setupUi(self, GeneralInputDialog):
        GeneralInputDialog.setObjectName("GeneralInputDialog")
        GeneralInputDialog.resize(333, 141)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GeneralInputDialog.sizePolicy().hasHeightForWidth())
        GeneralInputDialog.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        GeneralInputDialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(GeneralInputDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(GeneralInputDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.formLayout = QtWidgets.QFormLayout(self.frame)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_01 = QtWidgets.QLabel(self.frame)
        self.label_01.setObjectName("label_01")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_01)
        self.lineEdit_01 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_01.setObjectName("lineEdit_01")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_01)
        self.label_02 = QtWidgets.QLabel(self.frame)
        self.label_02.setObjectName("label_02")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_02)
        self.lineEdit_02 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_02.setObjectName("lineEdit_02")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_02)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.cbbAcType = QtWidgets.QComboBox(self.frame)
        self.cbbAcType.setObjectName("cbbAcType")
        self.cbbAcType.addItem("")
        self.cbbAcType.addItem("")
        self.cbbAcType.addItem("")
        self.cbbAcType.addItem("")
        self.cbbAcType.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cbbAcType)
        self.verticalLayout.addWidget(self.frame)
        self.buttonBox = QtWidgets.QDialogButtonBox(GeneralInputDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GeneralInputDialog)
        self.cbbAcType.setCurrentIndex(4)
        self.buttonBox.accepted.connect(GeneralInputDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(GeneralInputDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(GeneralInputDialog)

    def retranslateUi(self, GeneralInputDialog):
        _translate = QtCore.QCoreApplication.translate
        GeneralInputDialog.setWindowTitle(_translate("GeneralInputDialog", "Dialog"))
        self.label_01.setText(_translate("GeneralInputDialog", "TextLabel:"))
        self.label_02.setText(_translate("GeneralInputDialog", "TextLabel:"))
        self.label.setText(_translate("GeneralInputDialog", "AC_Type:"))
        self.cbbAcType.setItemText(0, _translate("GeneralInputDialog", "A306"))
        self.cbbAcType.setItemText(1, _translate("GeneralInputDialog", "A330"))
        self.cbbAcType.setItemText(2, _translate("GeneralInputDialog", "A350"))
        self.cbbAcType.setItemText(3, _translate("GeneralInputDialog", "B747"))
        self.cbbAcType.setItemText(4, _translate("GeneralInputDialog", "B777"))
