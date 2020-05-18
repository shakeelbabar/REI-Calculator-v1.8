from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

class Ui_Dialog(object):
    def setupUi(self, d):
        d.setObjectName("about_dialog")
        d.resize(700, 370)
        d.setStyleSheet("QDialog{\n"
"background-color:white;\n"
"}")
        self.Logo_prop = QtWidgets.QLabel(d)
        self.Logo_prop.setGeometry(QtCore.QRect(215, 20, 270, 250))
        self.Logo_prop.setText("")
        self.Logo_prop.setPixmap(QtGui.QPixmap("SFI-white.png"))
        self.Logo_prop.setScaledContents(True)
        self.Logo_prop.setAlignment(QtCore.Qt.AlignCenter)
        self.Logo_prop.setObjectName("Logo_prop")

        font = QtGui.QFont()
        font.setFamily("Calibri")  #Gill Sans MT Condensed
        font.setPointSize(13)
        font.setBold(True)
        # Name Label
        self.label_name = QtWidgets.QLabel(d)
        self.label_name.setGeometry(QtCore.QRect(0, 285, 700, 18))
        self.label_name.setFont(font)
        self.label_name.setAlignment(QtCore.Qt.AlignCenter)
        self.label_name.setAlignment(Qt.AlignCenter)
        self.label_name.setObjectName("label_name")
        # Version Label
        self.label_version = QtWidgets.QLabel(d)
        self.label_version.setGeometry(QtCore.QRect(0, 305, 700, 18))
        self.label_version.setFont(font)
        self.label_version.setAlignment(QtCore.Qt.AlignCenter)
        self.label_version.setAlignment(Qt.AlignCenter)
        self.label_version.setObjectName("label_version")
        # Version Label
        self.label_corporation = QtWidgets.QLabel(d)
        self.label_corporation.setGeometry(QtCore.QRect(0, 325, 700, 18))
        self.label_corporation.setFont(font)
        self.label_corporation.setAlignment(QtCore.Qt.AlignCenter)
        self.label_corporation.setObjectName("label_corporation")
        self.label_corporation.setStyleSheet("QLabel {color: #39974A;}")
        self.label_corporation.setAlignment(Qt.AlignCenter)
        # Version Label
        self.label_rights = QtWidgets.QLabel(d)
        self.label_rights.setGeometry(QtCore.QRect(0, 345, 700, 18))
        self.label_rights.setFont(font)
        self.label_rights.setAlignment(QtCore.Qt.AlignCenter)
        self.label_rights.setAlignment(Qt.AlignCenter)
        self.label_rights.setObjectName("label_rights")
        # self.label.setText("Name")
        # self.plainTextEdit = QtWidgets.QPlainTextEdit(d)
        # self.plainTextEdit.setEnabled(True)
        # self.plainTextEdit.setGeometry(QtCore.QRect(40, 120, 401, 321))
#         font = QtGui.QFont()
#         font.setFamily("Arial")
#         font.setPointSize(10)
#         self.plainTextEdit.setFont(font)
#         self.plainTextEdit.setStyleSheet("QPlainTextEdit{\n"
# "    border 0px solid black;\n"
# "}")
#         self.plainTextEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
#         self.plainTextEdit.setObjectName("plainTextEdit")

        self.retranslateUi(d)
        QtCore.QMetaObject.connectSlotsByName(d)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_name.setText(_translate("Dialog", "REI Buy & Hold Calculator"))
        self.label_version.setText(_translate("Dialog", "v1.10"))
        self.label_corporation.setText(_translate("Dialog", "Designed by Steiner Foresti Investment, LLC"))
        self.label_rights.setText(_translate("Dialog", "All Rights Reserved"))
        # self.plainTextEdit.setPlainText(_translate("Dialog", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."))



