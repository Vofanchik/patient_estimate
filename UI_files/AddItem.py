# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddItem.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddItem(object):
    def setupUi(self, AddItem):
        AddItem.setObjectName("AddItem")
        AddItem.resize(911, 366)
        self.gridLayout = QtWidgets.QGridLayout(AddItem)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(AddItem)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(AddItem)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(AddItem)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 3, 0, 1, 1)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(AddItem)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.doubleSpinBox.setFont(font)
        self.doubleSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox.setMaximum(999999.99)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.gridLayout.addWidget(self.doubleSpinBox, 5, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(AddItem)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(AddItem)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(AddItem)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 6, 0, 1, 1)

        self.retranslateUi(AddItem)
        QtCore.QMetaObject.connectSlotsByName(AddItem)

    def retranslateUi(self, AddItem):
        _translate = QtCore.QCoreApplication.translate
        AddItem.setWindowTitle(_translate("AddItem", "Добавить расходную позицию"))
        self.label.setText(_translate("AddItem", "Наименование"))
        self.label_2.setText(_translate("AddItem", "Еденица измерения"))
        self.label_3.setText(_translate("AddItem", "Цена за еденицу"))
        self.pushButton.setText(_translate("AddItem", "Добавить"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AddItem = QtWidgets.QDialog()
    ui = Ui_AddItem()
    ui.setupUi(AddItem)
    AddItem.show()
    sys.exit(app.exec_())
