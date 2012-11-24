#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from treenode.TreeNodeItemModel import TreeNodeItemModel
from SportBase import SportBase
from SequenceUi import Ui_Sequence
from SoundMgr import SoundMgr
from Exercise import *
from Series import *

class SequenceNode(SportBase):
    """ un commentaire"""
    def __init__(self, name='', parent=None):
        super(SequenceNode, self).__init__(name, parent)
        self._description = ""
        self._repetition = 1

    def description(self):
        return self._description

    def setDescription(self, description):
        assert isinstance(description, (str, unicode))
        self._description = description

    def repetition(self):
        return self._repetition

    def setRepetition(self, repetition):
        assert isinstance(repetition, int)
        self._repetition = repetition

    def play(self):
        print self._name
        if self._sound != None:
            SoundMgr().play(self._sound, self._duration)

class SequenceView(QDialog):
    def __init__(self, parent=None, sequence=None):
        super(SequenceView, self).__init__(parent)
        self.ui = Ui_Sequence()
        self.ui.setupUi(self)
        if sequence is None:
            self._sequence = SequenceNode("sequence")
        else:
            self._sequence = sequence
        self.ui.ldtName.setText(self._sequence.name())
        if isinstance(self._sequence.repetition(), int):
            self.ui.sbxRepetition.setValue(self._sequence.repetition())        
        
    def accept(self):
        self._sequence.setName(str(self.ui.ldtName.text()))
        self._sequence.setRepetition(self.ui.sbxRepetition.value())
        QDialog.accept(self)

    def getSequenceNode(self):
        assert isinstance(self._sequence, SequenceNode)
        return self._sequence

class SequenceCtl(QObject):
    def __init__ (self, parent = None):
        super(SequenceCtl, self).__init__(parent)        
        self.__initActions()
        self._current = None
        self._ctl = None
        self._cpt = 0

    def node(self):
        return self._sequence
    def setNode(self, sequence):
        assert isinstance(sequence, SequenceNode)
        self._sequence = sequence

    def model(self):
        return self._model
    def setModel(self, model):
        assert isinstance(model, TreeNodeItemModel)
        self._model = model
    def index(self):
        return self._index
    def setIndex(self, index):
        assert isinstance(index, QModelIndex)
        assert self._sequence == index.internalPointer()
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
        action = QAction("New sequence...", self)
        QObject.connect(action, SIGNAL("triggered()"), self.__newSequence)
        self._actions.append(action)
        action = QAction("separator", self)
        action.setSeparator(True)
        self._actions.append(action)
        action = QAction("Edit...", self)
        QObject.connect(action, SIGNAL("triggered()"), self.__editSequence)
        self._actions.append(action)
        action = QAction("Delete", self)
        QObject.connect(action, SIGNAL("triggered()"), self.__deleteSequence)
        self._actions.append(action)
        action = QAction("separator", self)
        action.setSeparator(True)
        self._actions.append(action)
        action = QAction("Play", self)
        QObject.connect(action, SIGNAL("triggered()"), self.play)
        self._actions.append(action)
            
    def populateMenu(self, menu):
        assert isinstance( menu, QMenu)        
        menu.addSeparator()
        action = QAction("[sequence] "+str(self._sequence.name()), self)
        font = QFont()
        font.setBold(True)
        action.setFont(font)
        menu.addAction(action)
        for item in self._actions:
            menu.addAction(item)

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
    def __newSequence(self):
        dlg = SequenceView(self.parent())
        if dlg.exec_():
            newSequence = dlg.getSequenceNode()
            self._model.insertNode(self._index, newSequence)
        pass

    def __editSequence(self):
        dlg = SequenceView(self.parent(), self._sequence)
        dlg.exec_()

    def play(self):
        if(self._cpt < self._sequence.repetition()):
            QObject.connect(self, SIGNAL('sequenceFinished()'), self.__nextSequence)
            self.__playSequence()
        else:
            self._cpt = 0
            self.emit(SIGNAL("finished()"))
        pass
    
    def __playSequence(self):
        assert isinstance(self._sequence, SequenceNode)
        assert self._ctl == None
        if self._current == None:
            self._current = self._sequence.child(0)
        else:
            self._current = self._current.nextSibling()
        node = self._current
        if node != None:
            print str(node)
            if node.type() == "ExerciseNode":
                self._ctl = ExerciseCtl(self)
            elif node.type() == "SeriesNode":
                self._ctl = SeriesCtl(self)
            elif node.type() == "SequenceNode":
                self._ctl = SequenceCtl(self)
            self._ctl.setNode(node)
            QObject.connect(self._ctl, SIGNAL('finished()'), self.__nextPlay)
            self._ctl.play()
        else:
            self.emit(SIGNAL("sequenceFinished()"))
        pass

    def __deleteSequence(self):        
        self._sequence.setIsDeleted(True)

    def __nextPlay(self):
        assert self._ctl != None
        print "nextPlay"
        QObject.disconnect(self._ctl, SIGNAL('finished()'), self.__nextPlay)
        self._ctl = None # disconnect
        self.__playSequence()

    def __nextSequence(self):
        QObject.disconnect(self, SIGNAL('sequenceFinished()'), self.__nextSequence)
        self._cpt += 1
        self.play()
