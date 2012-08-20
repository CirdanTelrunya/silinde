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

    def index(
        self,
        row,
        column,
        parent,
        ):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        if row < 0 or column < 0 or row >= self.rowCount(parent) \
            or column >= self.columnCount(parent):
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
        parentNode = childItem.parent()
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
            return str(node.name())

    def insertNode(self, parent, node):
        assert isinstance(node, TreeNode)
        parentNode = parent.internalPointer()
        if parentNode is None:
            parentNode = self._rootNode
        newRow = parentNode.childCount()
        # Insert the Node
        self.beginInsertRows(parent, newRow, newRow)
        parentNode.insertChild(node, newRow)
        self.endInsertRows()


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
