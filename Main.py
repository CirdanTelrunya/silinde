# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from gui_tree import Ui_GroupBox
from gui_dlgPackage import Ui_DlgPackage
from UML import *
from TreeNode import *

class DlgPackage(QDialog):
    def __init__(self, parent=None, package=None):
        super (DlgPackage, self).__init__(parent)
        self.ui = Ui_DlgPackage()
        self.ui.setupUi(self)
        
        if package is None:
            self._package = UmlPackage(parent, "Untitled")
        else:
            assert isinstance( package, UmlPackage)
            self.ui.ldtNom.setText(package.name())
            self._package = package

    def accept(self):
        self._package.setName(str(self.ui.ldtNom.text()))
        QDialog.accept(self)     

    def getNodePackage(self, parent):
        self._package.setParent(parent)
        return self._package

class CtlPackage(QObject):

    def __init__ (self, parent = None, model = None, index = None):
        super (CtlPackage, self).__init__(parent)
        assert isinstance( parent, QObject)
        assert isinstance( model, TreeItemModel)
        assert isinstance( index, QModelIndex)
        node = index.internalPointer()
        assert isinstance( node, UmlPackage)
        self._actions = []
        self._package = node
        self._model = model
        self._index = index
        action = QAction("Ajout Package...", self);
        QObject.connect(action, SIGNAL("triggered()"), self.ajoutPackage)
        self._actions.append(action)
        action = QAction("Edit Package...", self);
        QObject.connect(action, SIGNAL("triggered()"), self.editPackage)
        self._actions.append(action)

    def populate(self, menu):
        assert isinstance( menu, QMenu)
        for item in self._actions:
            menu.addAction(item)
        
    def ajoutPackage(self):
        dlg = DlgPackage()
        if dlg.exec_():
            newNode = dlg.getNodePackage(self._package)
            self._model.insertNode(self._index, newNode)
        pass
 
        
    def editPackage(self):
        dlg = DlgPackage(package = self._package)
        dlg.exec_()      


class TreeManipulator(QGroupBox):
    def __init__(self, parent=None):
        super (TreeManipulator, self).__init__(parent)
        self.ui = Ui_GroupBox()
        self.ui.setupUi(self)
        self.model = TreeItemModel(rootNode = UmlPackage(name = "Untitled"))
        self.ui.treeView.setModel(self.model)
        self.ui.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        
        QObject.connect(self.ui.treeView,SIGNAL('customContextMenuRequested(QPoint)'), self.ctxMenu)

            
    def ctxMenu(self, point):
        indices = self.ui.treeView.selectedIndexes()
        assert len(indices) == 1
        self.menu = QMenu(self.ui.treeView)
        node = indices[0].internalPointer()
        if node.type() == "UmlPackage":
            ctl = CtlPackage(self.menu, self.model, indices[0])
            ctl.populate(self.menu)
        self.menu.popup(self.ui.treeView.mapToGlobal(point))

if __name__ == "__main__":
	app = QApplication(sys.argv)
	myapp = TreeManipulator()
	myapp.show()
	sys.exit(app.exec_())
