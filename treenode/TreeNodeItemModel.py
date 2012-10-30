#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from TreeNode import TreeNode
import pickle
import string

class TreeNodeItemModel(QtCore.QAbstractItemModel):

    def __init__(self, rootNode=None, parent=None):
        assert isinstance(rootNode, TreeNode) or rootNode is None
        super(TreeNodeItemModel, self).__init__(parent)
        self._rootNode = TreeNode()
        if rootNode is None:
            self._rootNode.insertChild(TreeNode(name='Untitled',
                    parent=rootNode))
        else:
            self._rootNode.insertChild(rootNode)
	# end if
    # end def __init__

    def root(self):
        assert isinstance(self._rootNode, TreeNode)
        assert self._rootNode.childCount() == 1
        return self._rootNode.child(0)

    def index(
        self,
        row,
        column,
        parent,
        ):

        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
	# end if
        if row < 0 or column < 0 or row >= self.rowCount(parent) \
            or column >= self.columnCount(parent):
            return QtCore.QModelIndex()
	# end if
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()
	# end if
        childNode = parentNode.child(row)
        if childNode:
            return self.createIndex(row, column, childNode)
        else:
            return QtCore.QModelIndex()
	# end if
    # end def index

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()
	# end if
        childItem = index.internalPointer()
        parentNode = childItem.parent()
        if parentNode == self._rootNode:
            return QtCore.QModelIndex()
	# end if
        return self.createIndex(parentNode.row(), 0, parentNode)
    # end def parent

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0
	# end if
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()
	# end if
        return parentNode.childCount()
    # end def rowCount

    def columnCount(self, index):
        return 1
    # end def columnCount

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
	# end if
        node = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            return str(node.name())
        elif role == QtCore.Qt.DecorationRole:
            if node.icon() is not None:
                return QtGui.QIcon(node.icon())
        elif role == QtCore.Qt.FontRole:
            if(node.isDeleted()):
                font = QtGui.QFont()
                font.setStrikeOut(True)
                return font
        elif role == QtCore.Qt.SizeHintRole:
            return QtCore.QSize(32, 32)
	# end if
    # end def data

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(QtCore.QString("tree"))
        return None 

    def insertNode(self, parent, node, row = None):
        if not parent.isValid():
            return False
        assert isinstance(node, TreeNode)
        assert isinstance(parent, QtCore.QModelIndex)
        parentNode = parent.internalPointer()
        if parentNode is None:
            parentNode = self._rootNode
	# end if
        if row is None or row < 0 :
            row = parentNode.childCount()
        # Insert the Node
        self.beginInsertRows(parent, row, row)
        parentNode.insertChild(node, row)
        self.endInsertRows()
    # end def insertNode

    def removeRows(self, row, count, parent):
        
        if not parent.isValid():
            return False
        parentNode = parent.internalPointer()
        if parentNode is None:
            parentNode = self._rootNode
        
        self.beginRemoveRows(parent, row, row)
        parentNode.removeChild(row)
        self.endRemoveRows()

        return True

    def supportedDropActions(self):
        return QtCore.Qt.MoveAction 

    def flags(self, index):
        defaultFlags = QtCore.QAbstractItemModel.flags(self, index)
      
        if index.isValid():
            return QtCore.Qt.ItemIsDragEnabled | \
                    QtCore.Qt.ItemIsDropEnabled | defaultFlags
          
        else:
            return QtCore.Qt.ItemIsDropEnabled | defaultFlags

    def mimeTypes(self):
        types = QtCore.QStringList()
        types.append('text/plain')
        return types

    def mimeData(self, index):
        node = index[0].internalPointer()
        data = pickle.dumps(node)
        mimeData = QtCore.QMimeData()
        mimeData.setText(data)
        return mimeData 
        
    def dropMimeData(self, mimedata, action, row, column, parent):
        if not parent.isValid():
            return False
        node = parent.internalPointer()
        assert isinstance(node, TreeNode)
        newNode = pickle.loads(str(mimedata.text()))
        
        if action != QtCore.Qt.MoveAction:
            return False

        if node.canBeInserted(newNode):
            self.insertNode(parent, newNode, row)
            return True
        else:
            return False

# end class TreeNodeItemModel


if __name__ == '__main__':
    app = QtGui.QApplication([])
    root = TreeNode('Root')
    root.insertChild(TreeNode('Plup'))
    model = TreeNodeItemModel(root)
    dialog = QtGui.QDialog()
    dialog.setMinimumSize(300, 150)
    layout = QtGui.QVBoxLayout(dialog)
    tv = QtGui.QTreeView(dialog)
    tv.setModel(model)
    tv.dragEnabled()
    tv.acceptDrops()
    tv.showDropIndicator()
    tv.setDragDropMode(QtGui.QAbstractItemView.InternalMove) 
    

    layout.addWidget(tv)
    index = model.index(0, 0, QtCore.QModelIndex())
    model.insertNode(index, TreeNode('Plop'))
    model.insertNode(index, TreeNode('Plip'))
    dialog.exec_()
    app.closeAllWindows()
# end if
