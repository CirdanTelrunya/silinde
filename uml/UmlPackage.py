#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from UmlBase import UmlBase
from treenode.TreeNodeItemModel import TreeNodeItemModel
from UmlPackageUi import Ui_DlgPackage
from UmlClassView import *

class UmlPackageNode(UmlBase):
    """ un commentaire"""
    def __init__(self, name='', parent=None):
        super(UmlPackageNode, self).__init__(name, parent)
        
        # Contents
        self.stereotype = ""
        self.description = ""

class UmlPackageView(QDialog):
    def __init__(self, parent=None, package=None):
        super(UmlPackageView, self).__init__(parent)
        self.ui = Ui_DlgPackage()
        self.ui.setupUi(self)
        
        if package is None:
            self._package = UmlPackageNode("Untitled")
        else:
            assert isinstance( package, UmlPackageNode)
            self._package = package
        self.ui.ldtName.setText(self._package.name())

    def accept(self):
        self._package.setName(str(self.ui.ldtName.text()))
        QDialog.accept(self)

    def getPackageNode(self):
        assert isinstance(self._package, UmlPackageNode)
        return self._package


class UmlPackageCtl(QObject):
    def __init__ (self, parent = None, model = None, index = None):
        super(UmlPackageCtl, self).__init__(parent)
        assert isinstance( index, QModelIndex)
        assert isinstance( model, TreeNodeItemModel)
        self._package = index.internalPointer()
        self._model = model
        self._index = index
        self.__initActions()

    def populateMenu(self, menu):
        assert isinstance( menu, QMenu)
        
        menu.addSeparator()
        for item in self._actions:
            menu.addAction(item)

    def __initActions(self):
        self._actions = []
        action = QAction("[package] "+str(self._package.name()), self)
        font = QFont()
        font.setBold(True)
        action.setFont(font)
        self._actions.append(action)
        action = QAction("separator", self)
        action.setSeparator(True)
        self._actions.append(action)
        action = QAction("New package...", self)
        QObject.connect(action, SIGNAL("triggered()"), self.__newPackage)
        self._actions.append(action)
        action = QAction("New class view...", self)
        QObject.connect(action, SIGNAL("triggered()"), self.__newClassView)
        self._actions.append(action)
        action = QAction("separator", self)
        action.setSeparator(True)
        self._actions.append(action)
        action = QAction("Edit...", self)
        QObject.connect(action, SIGNAL("triggered()"), self.__editPackage)
        self._actions.append(action)
        action = QAction("Delete", self)
        QObject.connect(action, SIGNAL("triggered()"), self.__deletePackage)
        self._actions.append(action)

    def __newPackage(self):
        dlg = UmlPackageView()
        if dlg.exec_():
            newNode = dlg.getPackageNode()
            self._model.insertNode(self._index, newNode)

    def __newClassView(self):
        dlg = UmlClassViewView()
        if dlg.exec_():
            newNode = dlg.getClassViewNode()
            self._model.insertNode(self._index, newNode)            
            
    def __editPackage(self):
        dlg = UmlPackageView(package = self._package)
        dlg.exec_()
        pass

    def __deletePackage(self):
        pass    

        
class UmlPackageTree(QTreeView):
    def __init__ (self, parent = None):
        super(UmlPackageTree, self).__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        QObject.connect(self, SIGNAL('customContextMenuRequested(QPoint)'), self.ctxMenu)

    def ctxMenu(self, point):
        indices = self.selectedIndexes()
        assert len(indices) == 1
        node = indices[0].internalPointer()
        menu = QMenu(self)
        if node.type() == "UmlPackageNode":
            ctl = UmlPackageCtl(self, self.model(), indices[0])
            ctl.populateMenu(menu)
        elif node.type() == "UmlClassViewNode":
            ctl = UmlClassViewCtl(self, self.model(), indices[0])
            ctl.populateMenu(menu)            
        menu.popup(self.mapToGlobal(point))
        

if __name__ == '__main__':
    app = QApplication([])
    root = UmlPackageNode('package')
    model = TreeNodeItemModel(root)
    dialog = QDialog()
    dialog.setMinimumSize(300, 150)
    layout = QVBoxLayout(dialog)
    tv = UmlPackageTree(dialog)
    tv.setModel(model)
    tv.dragEnabled()
    tv.acceptDrops()
    tv.showDropIndicator()
    tv.setDragDropMode(QAbstractItemView.InternalMove) 
    layout.addWidget(tv)
    dialog.exec_()
    app.closeAllWindows()
# end if
