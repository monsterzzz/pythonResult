# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'watch.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_watch(object):
    def setupUi(self, watch):
        watch.setObjectName("watch")
        watch.resize(975, 718)
        self.qipan = QtWidgets.QGroupBox(watch)
        self.qipan.setGeometry(QtCore.QRect(10, 10, 741, 701))
        self.qipan.setObjectName("qipan")
        self.groupBox_2 = QtWidgets.QGroupBox(watch)
        self.groupBox_2.setGeometry(QtCore.QRect(760, 10, 201, 131))
        self.groupBox_2.setObjectName("groupBox_2")
        self.listWidget = QtWidgets.QListWidget(self.groupBox_2)
        self.listWidget.setGeometry(QtCore.QRect(10, 20, 181, 101))
        self.listWidget.setObjectName("listWidget")
        self.groupBox = QtWidgets.QGroupBox(watch)
        self.groupBox.setGeometry(QtCore.QRect(760, 140, 201, 371))
        self.groupBox.setObjectName("groupBox")
        self.listWidget_2 = QtWidgets.QListWidget(self.groupBox)
        self.listWidget_2.setGeometry(QtCore.QRect(10, 20, 181, 341))
        self.listWidget_2.setObjectName("listWidget_2")
        self.pushButton = QtWidgets.QPushButton(watch)
        self.pushButton.setGeometry(QtCore.QRect(800, 640, 111, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(watch)
        self.pushButton_2.setGeometry(QtCore.QRect(800, 560, 111, 41))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(watch)
        QtCore.QMetaObject.connectSlotsByName(watch)

    def retranslateUi(self, watch):
        _translate = QtCore.QCoreApplication.translate
        watch.setWindowTitle(_translate("watch", "Form"))
        self.qipan.setTitle(_translate("watch", "qipan"))
        self.groupBox_2.setTitle(_translate("watch", "GroupBox"))
        self.groupBox.setTitle(_translate("watch", "GroupBox"))
        self.pushButton.setText(_translate("watch", "leave"))
        self.pushButton_2.setText(_translate("watch", "list"))

