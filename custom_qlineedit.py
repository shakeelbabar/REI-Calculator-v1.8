from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import pyqtSignal

class MyQlineEdit(QLineEdit):
    
    focused = pyqtSignal()
    unfocused = pyqtSignal()

    def __init__(self, parent=None):
        super(MyQlineEdit, self).__init__(parent)
        
    def focusInEvent(self, event):
        self.focused.emit()
        super(MyQlineEdit, self).focusInEvent(event) 
        
    def focusOutEvent(self, event):
        self.unfocused.emit()
        super(MyQlineEdit, self).focusOutEvent(event) 
