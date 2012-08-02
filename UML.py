# -*- coding: utf-8 -*-
from TreeNode import TreeNode

class UmlPackage(TreeNode):
    def __init__(self, parent=None, name=""):
        super(UmlPackage, self).__init__(parent, name)
        
        # Contents
        self.stereotype = ""
        self.description = ""
        
        
class UmlClass(TreeNode):
    def __init__(self, parent=None):
        super(UmlClass, self).__init__(parent, name="")
        
        # Contents
        self.stereotype = ""
        self.description = ""

