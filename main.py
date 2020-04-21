from PyQt5 import QtWidgets
import sys

from REI_calc_main_design import Ui_MainWindow  

class CalculatorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(CalculatorWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = CalculatorWindow()
    application.show()
    sys.exit(app.exec())
