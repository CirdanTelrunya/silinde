#!/usr/bin/python
# -*- coding: utf-8 -*-

from treenode.TreeNode import TreeNode
from Logger import Logger

class SportBase(TreeNode):
    def __init__(self, name='', parent=None):
        super(SportBase, self).__init__(name, parent)
        self._isDeleted = False
        self._deletedIcon = None
        self._description = ""

    def deletedIcon(self):
        return self._deletedIcon
    
    def setDeletedIcon(self, path):
        assert isinstance(path, (str, unicode))
        self._deletedIcon = path

    def isDeleted(self):
        return self._isDeleted

    def setIsDeleted(self, deleted):
        assert isinstance(deleted, bool)
        self._isDeleted = deleted

    def description(self):
        return self._description

    def setDescription(self, description):
        assert isinstance(description, (str, unicode))
        self._description = description

    def __getstate__(self):
        odict = self.__dict__.copy()
        for child in self._children:
            if child.isDeleted():
                odict["_children"].remove(child)
        return odict

    def icon(self):
        if self.isDeleted() and self.deletedIcon() != None:
            return self.deletedIcon()
        else:
            return super(SportBase, self).icon()

    def log(self, logger):
        pass

    def populatePlaylist(self, playlist):
        pass
