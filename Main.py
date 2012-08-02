# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from gui_tree import Ui_GroupBox
from gui_dlgPackage import Ui_DlgPackage
from UML import *
from TreeNode import *

class DlgPackage(QDialog):
    def __init__(self, parent=None):
        super (DlgPackage, self).__init__(parent)
        self.ui = Ui_DlgPackage()
        self.ui.setupUi(self)
    def getNodePackage(self, parent):
        node = UmlPackage(parent, str(self.ui.ldtNom.text()))
        return node

class TreeManipulator(QGroupBox):
    def __init__(self, parent=None):
        super (TreeManipulator, self).__init__(parent)
        self.ui = Ui_GroupBox()
        self.ui.setupUi(self)
        self.model = TreeItemModel()
        self.ui.treeView.setModel(self.model)
        self.ui.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        

        #index = self.model.index(0,0, QtCore.QModelIndex( ))
        #self.model.insertNode(index)
        QObject.connect(self.ui.pushButton, SIGNAL("clicked()"), self.ajout)
        QObject.connect(self.ui.treeView,SIGNAL('customContextMenuRequested(QPoint)'), self.ctxMenu)

        self.actions = dict() 
        
        # action 1
        action = QAction("Ajout", self);
        QObject.connect(action, SIGNAL("triggered()"), self.ajout)
        self.actions["TreeNode"] = action
        # action 2
        action = QAction("Ajout Class", self);
        QObject.connect(action, SIGNAL("triggered()"), self.ajout)
        self.actions["UmlPackage"] = action
        
    def ajout(self):
        # get parent
        indices = self.ui.treeView.selectedIndexes()
        assert len(indices) == 1
        parentNode = indices[0].internalPointer()                
        dlg = DlgPackage()
        if dlg.exec_():
            newNode = dlg.getNodePackage(parentNode)
            self.model.insertNode(indices[0], newNode)
            
    def ctxMenu(self, point):
        indices = self.ui.treeView.selectedIndexes()
        assert len(indices) == 1
        node = indices[0].internalPointer()
        self.menu = QMenu(self.ui.treeView)
        typeNode = node.type()
        self.menu.addAction(self.actions[typeNode])
        self.menu.popup(self.ui.treeView.mapToGlobal(point))

if __name__ == "__main__":
	app = QApplication(sys.argv)
	myapp = TreeManipulator()
	myapp.show()
	sys.exit(app.exec_())
