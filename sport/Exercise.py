#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from treenode.TreeNodeItemModel import TreeNodeItemModel
from SportBase import SportBase
from ExerciseUi import Ui_Exercise
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
            SoundMgr().play(self._sound, self._duration)

class ExerciseView(QDialog):
    def __init__(self, parent=None, exercise=None):
        super(ExerciseView, self).__init__(parent)
        self.ui = Ui_Exercise()
        self.ui.setupUi(self)
        if exercise is None:
            self._exercise = ExerciseNode("exercise")
        else:
            self._exercise = exercise
        self.ui.ldtName.setText(self._exercise.name())
        if isinstance(self._exercise.duration(), (int, float)):
            self.ui.sbxDuration.setValue(self._exercise.duration())        
        sounds = SoundMgr().getList()
        for sound in sounds:
             self.ui.cbxSound.addItem(QString(sound))
        if self._exercise.sound() is not None:
            index = self.ui.cbxSound.findText(QString(self._exercise.sound()))
            if index != -1:
                self.ui.cbxSound.setCurrentIndex(index)
        
    def accept(self):
        self._exercise.setName(str(self.ui.ldtName.text()))
        self._exercise.setDuration(self.ui.sbxDuration.value())
        self._exercise.setSound(str(self.ui.cbxSound.currentText()))
        QDialog.accept(self)

    def getExerciseNode(self):
        assert isinstance(self._exercise, ExerciseNode)
        return self._exercise

class ExerciseCtl(QObject):
    def __init__ (self, parent = None):
        super(ExerciseCtl, self).__init__(parent)        
        self.__initActions()

    def node(self):
        return self._exercise
    def setNode(self, exercise):
        assert isinstance(exercise, ExerciseNode)
        self._exercise = exercise

    def __initActions(self):
        self._actions = []
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
        action = QAction("[exercise] "+str(self._exercise.name()), self)
        font = QFont()
        font.setBold(True)
        action.setFont(font)
        for item in self._actions:
            menu.addAction(item)

    def __editExercise(self):
        dlg = ExerciseView(self.parent(), self._exercise)
        dlg.exec_()

    def __playExercise(self):
        self._exercise.play()
