#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from treenode.TreeNodeItemModel import TreeNodeItemModel
from SportBase import SportBase
from TrainingUi import Ui_TrainingView
from Exercise import *
from Series import *
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
    def __init__ (self, parent = None, index = None):
        super(TrainingCtl, self).__init__(parent)
        self.__initActions()

    def node(self):
        return self._training

    def setNode(self, training):
        assert isinstance(training, TrainingNode)
        self._training = training

    def model(self):
        return self._model
    def setModel(self, model):
        assert isinstance(model, TreeNodeItemModel)
        self._model = model
    def index(self):
        return self._index
    def setIndex(self, index):
        assert isinstance(index, QModelIndex)
        assert self._training == index.internalPointer()
        self._index = index


    def __initActions(self):
        self._actions = []        
        action = QAction("separator", self)
        action.setSeparator(True)
        self._actions.append(action)
        action = QAction("New exercise...", self)
        QObject.connect(action, SIGNAL("triggered()"), self.__newExercise)
        self._actions.append(action)
        action = QAction("New series...", self)
        QObject.connect(action, SIGNAL("triggered()"), self.__newSeries)
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

    def __newSeries(self):
        dlg = SeriesView(self.parent())
        if dlg.exec_():
            newSeries = dlg.getSeriesNode()
            self._model.insertNode(self._index, newSeries)
        pass

    
    def __editTraining(self):
        dlg = TrainingView(self.parent(), self._training)
        dlg.exec_()
        pass
    def __deleteTraining(self):
        pass

    def populateMenu(self, menu):
        assert isinstance(menu, QMenu)        
        menu.addSeparator()
        action = QAction("[training] "+str(self._training.name()), self)
        font = QFont()
        font.setBold(True)
        action.setFont(font)
        menu.addAction(action)
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
        self._controlers = dict()
        self._controlers["TrainingNode"] = TrainingCtl(self)
        self._controlers["ExerciseNode"] = ExerciseCtl(self)
        self._controlers["SeriesNode"] = SeriesCtl(self)

    def ctxMenu(self, point):
        indices = self.selectedIndexes()
        assert len(indices) == 1
        node = indices[0].internalPointer()
        print node.type()
        menu = QMenu(self)
        ctl = self._controlers[node.type()]        
        ctl.setNode(node)
        if node.type() == "TrainingNode":
            ctl.setModel(self.model())
            ctl.setIndex(indices[0])
        
        ctl.populateMenu(menu)
        menu.exec_(self.mapToGlobal(point))
        menu.deleteLater()
        pass


if __name__ == '__main__':
    app = QApplication([])
    soundMgr = SoundMgr()
    soundMgr.add('anvil', '/usr/lib/openoffice/basis3.2/share/gallery/sounds/ANVIL.WAV')
    soundMgr.add('kling', '/usr/lib/openoffice/basis3.2/share/gallery/sounds/kling.wav')
    # soundMgr.add('kling', '/usr/lib/libreoffice/basis3.3/share/gallery/sounds/kling.wav')
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
    SoundMgr.instance = None
