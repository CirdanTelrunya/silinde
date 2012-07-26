# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore

class TreeNode( object ):
    def __init__(self, parent=None, data=None):
        assert isinstance( parent, TreeNode) or (parent is None)

        # Contents
        self._data = data
        # Structure
        self._parentNode = parent
        self._childNodes = []

    def appendChild(self, node):
        assert isinstance( node, TreeNode )
      
        node._parentNode = self
        self._childNodes.append(node)

    def setData( self, value ):
        self._data = value
 
    def getData( self ):
        return self._data

    def row(self):
        if self._parentNode:
            return self._parentNode._childNodes.index(self)      
        return 0

    def parent( self ):
        return self._parentNode
    def child(self, row):
        return self._childNodes[row]
    def childCount(self):
        return len(self._childNodes)
    
class TreeItemModel(QtCore.QAbstractItemModel):
    def __init__(self, rootNode=None, parent=None):
        super(TreeItemModel, self).__init__(parent)
        if rootNode is None:
            rootNode = TreeNode( data='FakeRoot' )
            rootNode.appendChild( TreeNode( data='Untitled', parent=rootNode ) )
        self._rootNode       = rootNode
        
    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        if row < 0 or column < 0 or row >= self.rowCount(parent) or column >= self.columnCount(parent):
            return QtCore.QModelIndex()
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()
            
        childNode = parentNode.child(row)
        if childNode:
            return self.createIndex(row, column, childNode)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()
      
        childItem = index.internalPointer()
        parentNode = childItem._parentNode
      
        if parentNode == self._rootNode:
            return QtCore.QModelIndex()
      
        return self.createIndex(parentNode.row(), 0, parentNode)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0
      
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()
            
        return parentNode.childCount()

    def columnCount(self, index):
        return 1

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()

        node = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            return str(node.getData())
        
        return QtCore.QVariant()

    def insertNode( self, parent):
        parentNode = parent.internalPointer()
        if parentNode is None:
            parentNode = self._rootNode
        children = parentNode._childNodes
        newNode = TreeNode( data='TEST', parent=parentNode )
        newRow = parentNode.childCount()
        # Insert the Node
        self.beginInsertRows( parent, newRow, newRow )
        children.insert(newRow, newNode)
        self.endInsertRows( )
    
if __name__ == "__main__":
    app = QtGui.QApplication([])
    model = TreeItemModel()
    dialog = QtGui.QDialog()
    dialog.setMinimumSize(300,150)
    layout = QtGui.QVBoxLayout(dialog)
    tv = QtGui.QTreeView(dialog)
    tv.setModel(model)
    layout.addWidget(tv)
    index = model.index(0,0, QtCore.QModelIndex( ))
    model.insertNode(index)
    
    dialog.exec_()

    
    

    app.closeAllWindows()
    
