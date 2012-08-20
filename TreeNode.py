#!/usr/bin/python
# -*- coding: utf-8 -*-

from uuid import uuid4


class TreeNode(object):

    def __init__(self, name='', parent=None):
        assert isinstance(parent, TreeNode) or parent is None
        assert isinstance(name, (str, unicode))
        # Contents
        self._name = name
        self._type = self.__class__.__name__
        self._id = uuid4().hex
        # Structure
        self._parent = parent
        self._children = []

    def __str__(self):
        assert isinstance(self._name, (str, unicode))
        return _name

    def insertChild(self, node, row = None):
        assert isinstance(node, TreeNode)
        node._parent = self
        if row is None:
            self._children.append(node)
        else:
            assert isinstance(row, int)
            self._children.insert(row, node)

    def name(self):
        assert isinstance(self._name, (str, unicode))
        return self._name

    def setName(self, name='Untitled'):
        assert isinstance(name, (str, unicode))
        self._name = name

    def type(self):
        assert isinstance(self._type, (str, unicode))
        return self._type

    def id(self):
        return self._id

    def parent(self):
        return self._parent

    def setParent(self, parent):
        assert isinstance(parent, TreeNode)
        self._parent = parent

    def child(self, row):
        return self._children[row]

    def children(self):
        return self._children


    def childCount(self):
        return len(self._children)

    def row(self):
        if self._parent:
            return self._parent._children.index(self)
        return 0


