#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from treenode.TreeNodeItemModel import TreeNodeItemModel
from SportBase import SportBase
from TrainingUi import Ui_TrainingView
from Exercise import *
from SoundMgr import SoundMgr

class TrainingNode(SportBase):
    """ un commentaire"""
    def __init__(self, name='', parent=None):
        super(TrainingNode, self).__init__(name, parent)
        self._description = ""
        
    def setDescription(self, description):
        assert isinstance(description, (str, unicode))
        self._description = description

    def description(self):
        assert isinstance(self._description, (str, unicode))
        return self._description

class TrainingView(QDialog):
    def __init__(self, parent=None, training=None):
        super(TrainingView, self).__init__(parent)
        self.ui = Ui_TrainingView()
        self.ui.setupUi(self)
        if training is None:
            self._training = TrainingNode("training")
        else:
            assert isinstance(training, TrainingNode)
            self._training = training
        self.ui.ldtName.setText(self._training.name())
        self.ui.tdtDescription.setPlainText(self._training.description())

    def accept(self):
        self._training.setName(str(self.ui.ldtName.text()))
        self._training.setDescription(str(self.ui.tdtDescription.toPlainText()))
        QDialog.accept(self)

class TrainingCtl(QObject):
    def __init__ (self, parent = None, model = None, index = None):
        super(TrainingCtl, self).__init__(parent)
        assert isinstance(index, QModelIndex)
        assert isinstance(model, TreeNodeItemModel)
        self._training = index.internalPointer()
        assert isinstance(self._training, TrainingNode)
        self._model = model
        self._index = index
        self.__initActions()

    def __initActions(self):
        self._actions = []
        action = QAction("[training] "+str(self._training.name()), self)
        font = QFont()
        font.setBold(True)
        action.setFont(font)
        self._actions.append(action)
        action = QAction("separator", self)
        action.setSeparator(True)
        self._actions.append(action)
        action = QAction("New exercise...", self)
        QObject.connect(action, SIGNAL("triggered()"), self.__newExercise)
        self._actions.append(action)
        action = QAction("separator", self)
        action.setSeparator(True)
        self._actions.append(action)
        action = QAction("Edit...", self)
        QObject.connect(action, SIGNAL("triggered()"), self.__editTraining)
        self._actions.append(action)
        action = QAction("Delete", self)
        QObject.connect(action, SIGNAL("triggered()"), self.__deleteTraining)
        self._actions.append(action)

    def __newExercise(self):
        dlg = ExerciseView(self.parent())
        if dlg.exec_():
            newExercise = dlg.getExerciseNode()
            self._model.insertNode(self._index, newExercise)
        pass
    
    def __editTraining(self):
        dlg = TrainingView(self.parent(), self._training)
        dlg.exec_()
        pass
    def __deleteTraining(self):
        pass

    def populateMenu(self, menu):
        assert isinstance( menu, QMenu)        
        menu.addSeparator()
        for item in self._actions:
            menu.addAction(item)

class TrainingTree(QTreeView):
    def __init__ (self, parent = None):
        super(TrainingTree, self).__init__(parent)
        self.dragEnabled()
        self.acceptDrops()
        self.showDropIndicator()
        self.setDragDropMode(QAbstractItemView.InternalMove) 
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        QObject.connect(self, SIGNAL('customContextMenuRequested(QPoint)'), self.ctxMenu)
        

    def ctxMenu(self, point):
        indices = self.selectedIndexes()
        assert len(indices) == 1
        node = indices[0].internalPointer()
        menu = QMenu(self)
        if node.type() == "TrainingNode":
            ctl = TrainingCtl(self, self.model(), indices[0])
            ctl.populateMenu(menu)
        elif node.type() == "ExerciseNode":
            ctl = ExerciseCtl(self, self.model(), indices[0])
            ctl.populateMenu(menu)
        menu.popup(self.mapToGlobal(point))
        pass


if __name__ == '__main__':
    app = QApplication([])
    soundMgr = SoundMgr()
    soundMgr.add('anvil', '/usr/lib/openoffice/basis3.2/share/gallery/sounds/ANVIL.WAV')
    soundMgr.add('kling', '/usr/lib/openoffice/basis3.2/share/gallery/sounds/kling.wav')
    root = TrainingNode('training')
    model = TreeNodeItemModel(root)
    dialog = QDialog()
    dialog.setMinimumSize(300, 150)
    layout = QVBoxLayout(dialog)
    tv = TrainingTree(dialog)
    tv.setModel(model)
    layout.addWidget(tv)
    dialog.exec_()
    app.closeAllWindows()
