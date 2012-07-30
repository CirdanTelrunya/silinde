# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from tree_gui import Ui_GroupBox
from TreeNode import *

class TreeManipulator(QGroupBox):
    def __init__(self, parent=None):
        super (TreeManipulator, self).__init__(parent)
        self.ui = Ui_GroupBox()
        self.ui.setupUi(self)
        self.model = TreeItemModel()
        self.ui.treeView.setModel(self.model)
        #index = self.model.index(0,0, QtCore.QModelIndex( ))
        #self.model.insertNode(index)
        QObject.connect(self.ui.pushButton, SIGNAL("clicked()"), self.ajout)

    def ajout(self):
        indices = self.ui.treeView.selectedIndexes()
        if len(indices) == 1:
            self.model.insertNode(indices[0])

if __name__ == "__main__":
	app = QApplication(sys.argv)
	myapp = TreeManipulator()
	myapp.show()
	sys.exit(app.exec_())
