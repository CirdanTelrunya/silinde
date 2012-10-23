#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from MainWindowUi import Ui_MainWindow
import sys

class MainWindow(QMainWindow):
    def __init__ (self, parent = None, flags = 0):
        super(MainWindow, self).__init__(parent, Qt.WindowFlags(flags))
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
    
