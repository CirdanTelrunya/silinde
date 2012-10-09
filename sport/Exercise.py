#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from treenode.TreeNodeItemModel import TreeNodeItemModel
from SportBase import SportBase
from ExerciseUi import Ui_ExerciseView
from SoundMgr import SoundMgr

class ExerciseNode(SportBase):
    """ un commentaire"""
    def __init__(self, name='', parent=None):
        super(ExerciseNode, self).__init__(name, parent)
        self._description = ""
        self._duration = None
        self._sound = None

    def description(self):
        return self._description

    def setDescription(self, description):
        assert isinstance(description, (str, unicode))
        self._description = description

    def duration(self):
        return self._duration

    def setDuration(self, duration):
        assert isinstance(duration, (int, float))
        self._duration = duration

    def sound(self):
        return self._sound

    def setSound(self, sound):
        assert isinstance(sound, (str, unicode))
        self._sound = sound

    def play(self):
        print self._name
        if self._sound != None:
            SoundMgr().play(self._sound)

class ExerciseView(QDialog):
    def __init__(self, parent=None, exercise=None):
        super(ExerciseView, self).__init__(parent)
        self.ui = Ui_ExerciseView()
        self.ui.setupUi(self)
        if exercise is None:
            self._exercise = ExerciseNode("exercise")
        else:
            self._exercise = exercise
        self.ui.ldtName.setText(self._exercise.name())
        if isinstance(self._exercise.duration(), float):
            self.ui.sbxDuration.setValue(self._exercise.duration())
        if self._exercise.sound() is not None:
            self.ui.cbxSound.addItem(self._exercise.sound())
        completer = QCompleter(SoundMgr().getList())
        self.ui.cbxSound.setCompleter(completer)
        
    def accept(self):
        self._exercise.setName(str(self.ui.ldtName.text()))
        self._exercise.setDuration(self.ui.sbxDuration.value())
        self._exercise.setSound(str(self.ui.cbxSound.currentText()))
        QDialog.accept(self)

    def getExerciseNode(self):
        assert isinstance(self._exercise, ExerciseNode)
        return self._exercise

class ExerciseCtl(QObject):
    def __init__ (self, parent = None, model = None, index = None):
        super(ExerciseCtl, self).__init__(parent)
        assert isinstance(index, QModelIndex)
        assert isinstance(model, TreeNodeItemModel)
        self._exercise = index.internalPointer()
        assert isinstance(self._exercise, ExerciseNode)
        self._model = model
        self._index = index
        self.__initActions()

    def __initActions(self):
        self._actions = []
        action = QAction("[exercise] "+str(self._exercise.name()), self)
        font = QFont()
        font.setBold(True)
        action.setFont(font)
        self._actions.append(action)
        action = QAction("separator", self)
        action.setSeparator(True)
        self._actions.append(action)
        action = QAction("Edit...", self)
        QObject.connect(action, SIGNAL("triggered()"), self.__editExercise)
        self._actions.append(action)
        action = QAction("Play", self)
        QObject.connect(action, SIGNAL("triggered()"), self.__playExercise)
        self._actions.append(action)
    
    def populateMenu(self, menu):
        assert isinstance( menu, QMenu)        
        menu.addSeparator()
        for item in self._actions:
            menu.addAction(item)

    def __editExercise(self):
        dlg = ExerciseView(self.parent(), self._exercise)
        dlg.exec_()

    def __playExercise(self):
        self._exercise.play()
