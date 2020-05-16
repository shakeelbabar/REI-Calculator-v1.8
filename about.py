from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, d):
        d.setObjectName("about_dialog")
        d.resize(484, 474)
        d.setStyleSheet("QDialog{\n"
"background-color:white;\n"
"}")
        self.Logo_prop = QtWidgets.QLabel(d)
        self.Logo_prop.setGeometry(QtCore.QRect(0, 0, 121, 101))
        self.Logo_prop.setText("")
        self.Logo_prop.setPixmap(QtGui.QPixmap("SFI-white.png"))
        self.Logo_prop.setScaledContents(True)
        self.Logo_prop.setAlignment(QtCore.Qt.AlignCenter)
        self.Logo_prop.setObjectName("Logo_prop")
        print("here1")
        self.label = QtWidgets.QLabel(d)
        self.label.setGeometry(QtCore.QRect(150, 30, 231, 41))
        font = QtGui.QFont()
        font.setFamily("Gill Sans MT Condensed")
        font.setPointSize(36)
        print("here2")
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        print("here3")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(d)
        self.plainTextEdit.setEnabled(True)
        self.plainTextEdit.setGeometry(QtCore.QRect(40, 120, 401, 321))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        print("here4")
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setStyleSheet("QPlainTextEdit{\n"
"    border 0px solid black;\n"
"}")
        print("here5")
        self.plainTextEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.retranslateUi(d)
        QtCore.QMetaObject.connectSlotsByName(d)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "REI CALCULATOR"))
        self.plainTextEdit.setPlainText(_translate("Dialog", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."))



