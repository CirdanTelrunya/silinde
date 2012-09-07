#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from treenode.TreeNode import TreeNode
from treenode.TreeNodeItemModel import TreeNodeItemModel
from UmlClassViewUi import Ui_DlgClassView

class UmlClassViewNode(TreeNode):
    """ un commentaire"""
    def __init__(self, name='', parent=None):
        super(UmlClassViewNode, self).__init__(name, parent)
        
        # Contents
        self.stereotype = ""
        self.description = ""
        self.deployement = None

class UmlClassViewView(QDialog):
    def __init__(self, parent=None, classView=None):
        super(UmlClassViewView, self).__init__(parent)
        self.ui = Ui_DlgClassView()
        self.ui.setupUi(self)
        
        if classView is None:
            self._classView = UmlClassViewNode("Untitled")
        else:
            assert isinstance(classView, UmlClassViewNode)
            self._classView = classView
        self.ui.ldtName.setText(self._classView.name())

    def accept(self):
        self._classView.setName(str(self.ui.ldtName.text()))
        QDialog.accept(self)

    def getClassViewNode(self):
        assert isinstance(self._classView, UmlClassViewNode)
        return self._classView

class UmlClassViewCtl(QObject):
    def __init__ (self, parent = None, model = None, index = None):
        super(UmlClassViewCtl, self).__init__(parent)
        assert isinstance( index, QModelIndex)
        assert isinstance( model, TreeNodeItemModel)
        self._classView = index.internalPointer()
        assert isinstance(self._classView, UmlClassViewNode)
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
        action = QAction("[class view] "+str(self._classView.name()), self)
        font = QFont()
        font.setBold(True)
        action.setFont(font)
        self._actions.append(action)
        action = QAction("separator", self)
        action.setSeparator(True)
        self._actions.append(action)
        action = QAction("Edit...", self)
        QObject.connect(action, SIGNAL("triggered()"), self.__editClassView)
        self._actions.append(action)
        action = QAction("Delete", self)
        QObject.connect(action, SIGNAL("triggered()"), self.__deleteClassView)
        self._actions.append(action)
        
            
    def __editClassView(self):
        dlg = UmlClassViewView(classView = self._classView)
        dlg.exec_()
        pass

    def __deleteClassView(self):
        pass    

