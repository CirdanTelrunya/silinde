#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from TreeNode import TreeNode


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
	# end if
    # end def data

    def insertNode(self, parent, node):
        assert isinstance(node, TreeNode)
        parentNode = parent.internalPointer()
        if parentNode is None:
            parentNode = self._rootNode
	# end if
        newRow = parentNode.childCount()
        # Insert the Node
        self.beginInsertRows(parent, newRow, newRow)
        parentNode.insertChild(node, newRow)
        self.endInsertRows()
    # end def insertNode
# end class TreeNodeItemModel


if __name__ == '__main__':
    app = QtGui.QApplication([])
    model = TreeNodeItemModel(TreeNode('Root'))
    dialog = QtGui.QDialog()
    dialog.setMinimumSize(300, 150)
    layout = QtGui.QVBoxLayout(dialog)
    tv = QtGui.QTreeView(dialog)
    tv.setModel(model)
    layout.addWidget(tv)
    index = model.index(0, 0, QtCore.QModelIndex())
    model.insertNode(index, TreeNode('Plop'))
    dialog.exec_()
    app.closeAllWindows()
# end if
