# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newreferencedialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NewReferenceDialog(object):
    def setupUi(self, NewReferenceDialog):
        NewReferenceDialog.setObjectName("NewReferenceDialog")
        NewReferenceDialog.resize(343, 130)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NewReferenceDialog.sizePolicy().hasHeightForWidth())
        NewReferenceDialog.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        NewReferenceDialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(NewReferenceDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(NewReferenceDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.formLayout = QtWidgets.QFormLayout(self.frame)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.leProcedure = QtWidgets.QLineEdit(self.frame)
        self.leProcedure.setReadOnly(True)
        self.leProcedure.setObjectName("leProcedure")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.leProcedure)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.cbbType = QtWidgets.QComboBox(self.frame)
        self.cbbType.setEditable(True)
        self.cbbType.setObjectName("cbbType")
        self.cbbType.addItem("")
        self.cbbType.setItemText(0, "")
        self.cbbType.addItem("")
        self.cbbType.addItem("")
        self.cbbType.addItem("")
        self.cbbType.addItem("")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cbbType)
        self.leReference = QtWidgets.QLineEdit(self.frame)
        self.leReference.setObjectName("leReference")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.leReference)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.verticalLayout.addWidget(self.frame)
        self.buttonBox = QtWidgets.QDialogButtonBox(NewReferenceDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(NewReferenceDialog)
        self.buttonBox.accepted.connect(NewReferenceDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(NewReferenceDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(NewReferenceDialog)

    def retranslateUi(self, NewReferenceDialog):
        _translate = QtCore.QCoreApplication.translate
        NewReferenceDialog.setWindowTitle(_translate("NewReferenceDialog", "Dialog"))
        self.label_2.setText(_translate("NewReferenceDialog", "Reference:"))
        self.label_3.setText(_translate("NewReferenceDialog", "Type:"))
        self.cbbType.setItemText(1, _translate("NewReferenceDialog", "AMM"))
        self.cbbType.setItemText(2, _translate("NewReferenceDialog", "AD"))
        self.cbbType.setItemText(3, _translate("NewReferenceDialog", "SB"))
        self.cbbType.setItemText(4, _translate("NewReferenceDialog", "MRB"))
        self.label.setText(_translate("NewReferenceDialog", "Procedure_ID:"))
