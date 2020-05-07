# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.setWindowModality(QtCore.Qt.WindowModal)
        SettingsDialog.resize(299, 196)
        self.save_button = QtWidgets.QPushButton(SettingsDialog)
        self.save_button.setGeometry(QtCore.QRect(220, 160, 75, 31))
        self.save_button.setFlat(False)
        self.save_button.setObjectName("save_button")
        self.bgcolor_groupbox = QtWidgets.QGroupBox(SettingsDialog)
        self.bgcolor_groupbox.setGeometry(QtCore.QRect(10, 10, 281, 141))
        self.bgcolor_groupbox.setObjectName("bgcolor_groupbox")
        self.special_row_bgcolor_label = QtWidgets.QLabel(self.bgcolor_groupbox)
        self.special_row_bgcolor_label.setGeometry(QtCore.QRect(30, 70, 111, 19))
        self.special_row_bgcolor_label.setObjectName("special_row_bgcolor_label")
        self.caption_bgcolor_label = QtWidgets.QLabel(self.bgcolor_groupbox)
        self.caption_bgcolor_label.setGeometry(QtCore.QRect(30, 40, 91, 19))
        self.caption_bgcolor_label.setObjectName("caption_bgcolor_label")
        self.caption_bgcolor_button = QtWidgets.QPushButton(self.bgcolor_groupbox)
        self.caption_bgcolor_button.setGeometry(QtCore.QRect(130, 30, 61, 35))
        self.caption_bgcolor_button.setObjectName("caption_bgcolor_button")
        self.special_row_bgcolor_button = QtWidgets.QPushButton(self.bgcolor_groupbox)
        self.special_row_bgcolor_button.setGeometry(QtCore.QRect(130, 70, 61, 35))
        self.special_row_bgcolor_button.setObjectName("special_row_bgcolor_button")

        self.retranslateUi(SettingsDialog)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        SettingsDialog.setWindowTitle(_translate("SettingsDialog", "Settings"))
        self.save_button.setText(_translate("SettingsDialog", "Save"))
        self.bgcolor_groupbox.setTitle(_translate("SettingsDialog", "Row background color"))
        self.special_row_bgcolor_label.setText(_translate("SettingsDialog", "Special rows:"))
        self.caption_bgcolor_label.setText(_translate("SettingsDialog", "Captions:"))
        self.caption_bgcolor_button.setText(_translate("SettingsDialog", "color"))
        self.special_row_bgcolor_button.setText(_translate("SettingsDialog", "color"))
