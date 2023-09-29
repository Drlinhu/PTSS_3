# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mhnrctbcinputdialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MhNrcTbcInputDialog(object):
    def setupUi(self, MhNrcTbcInputDialog):
        MhNrcTbcInputDialog.setObjectName("MhNrcTbcInputDialog")
        MhNrcTbcInputDialog.setWindowModality(QtCore.Qt.WindowModal)
        MhNrcTbcInputDialog.resize(354, 197)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        MhNrcTbcInputDialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(MhNrcTbcInputDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(MhNrcTbcInputDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.formLayout = QtWidgets.QFormLayout(self.frame)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEditNrcId = QtWidgets.QLineEdit(self.frame)
        self.lineEditNrcId.setReadOnly(True)
        self.lineEditNrcId.setObjectName("lineEditNrcId")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEditNrcId)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.doubleSpinBoxCharged = QtWidgets.QDoubleSpinBox(self.frame)
        self.doubleSpinBoxCharged.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxCharged.setMinimum(-1.0)
        self.doubleSpinBoxCharged.setMaximum(10000.0)
        self.doubleSpinBoxCharged.setSingleStep(0.5)
        self.doubleSpinBoxCharged.setObjectName("doubleSpinBoxCharged")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxCharged)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.plainTextEditRemark = QtWidgets.QPlainTextEdit(self.frame)
        self.plainTextEditRemark.setObjectName("plainTextEditRemark")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.plainTextEditRemark)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.doubleSpinBoxAgreed = QtWidgets.QDoubleSpinBox(self.frame)
        self.doubleSpinBoxAgreed.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxAgreed.setMinimum(-1.0)
        self.doubleSpinBoxAgreed.setMaximum(10000.0)
        self.doubleSpinBoxAgreed.setSingleStep(0.5)
        self.doubleSpinBoxAgreed.setObjectName("doubleSpinBoxAgreed")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxAgreed)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.cbbEngineer = QtWidgets.QComboBox(self.frame)
        self.cbbEngineer.setEditable(True)
        self.cbbEngineer.setObjectName("cbbEngineer")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.cbbEngineer)
        self.verticalLayout.addWidget(self.frame)
        self.buttonBox = QtWidgets.QDialogButtonBox(MhNrcTbcInputDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(MhNrcTbcInputDialog)
        self.buttonBox.accepted.connect(MhNrcTbcInputDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(MhNrcTbcInputDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MhNrcTbcInputDialog)

    def retranslateUi(self, MhNrcTbcInputDialog):
        _translate = QtCore.QCoreApplication.translate
        MhNrcTbcInputDialog.setWindowTitle(_translate("MhNrcTbcInputDialog", "TBC Input Dialog"))
        self.label.setText(_translate("MhNrcTbcInputDialog", "NRC_ID:"))
        self.label_2.setText(_translate("MhNrcTbcInputDialog", "Charged:"))
        self.label_3.setText(_translate("MhNrcTbcInputDialog", "Remark:"))
        self.label_4.setText(_translate("MhNrcTbcInputDialog", "Agreed:"))
        self.label_5.setText(_translate("MhNrcTbcInputDialog", "Engineer"))
