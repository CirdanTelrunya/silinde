#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from treenode.TreeNodeItemModel import TreeNodeItemModel
from SportBase import SportBase
from SeriesUi import Ui_Series
from SoundMgr import SoundMgr

class SeriesNode(SportBase):
    """ un commentaire"""
    def __init__(self, name='', parent=None):
        super(SeriesNode, self).__init__(name, parent)
        self._description = ""
        self._repetition = None
        self._duration = None
        self._sound = None
        self.setIcon(":/icons/series.png")
        self.setDeletedIcon(":/icons/series_delete.png")

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
            for i in range(self._repetition):
                SoundMgr().play(self._sound, self._duration)

class SeriesView(QDialog):
    def __init__(self, parent=None, series=None):
        super(SeriesView, self).__init__(parent)
        self.ui = Ui_Series()
        self.ui.setupUi(self)
        if series is None:
            self._series = SeriesNode("series")
        else:
            assert isinstance(series, SeriesNode)
            self._series = series
        self.ui.ldtName.setText(self._series.name())
        if isinstance(self._series.repetition(), int):
            self.ui.sbxRepetition.setValue(self._series.repetition())
        if isinstance(self._series.duration(), (int, float)):
            self.ui.sbxDuration.setValue(self._series.duration())        
        sounds = SoundMgr().getList()
        for sound in sounds:
            self.ui.cbxSound.addItem(QString(sound)) 
        if self._series.sound() is not None:
            index = self.ui.cbxSound.findText(QString(self._series.sound()))
            if index != -1:
                self.ui.cbxSound.setCurrentIndex(index)        
    def accept(self):
        self._series.setName(str(self.ui.ldtName.text()))
        self._series.setRepetition(self.ui.sbxRepetition.value())
        self._series.setDuration(self.ui.sbxDuration.value())
        self._series.setSound(str(self.ui.cbxSound.currentText()))
        QDialog.accept(self)
    def getSeriesNode(self):
        assert isinstance(self._series, SeriesNode)
        return self._series

class SeriesCtl(QObject):
    def __init__ (self, parent = None):
        super(SeriesCtl, self).__init__(parent)        
        self.__initActions()

    def node(self):
        return self._series
    
    def setNode(self, series):
        assert isinstance(series, SeriesNode)
        self._series = series

    def __del__(self):
        print "__del__SeriesCtl"

    def __initActions(self):
        self._actions = []        
        action = QAction("separator", self)
        action.setSeparator(True)
        self._actions.append(action)
        action = QAction("Edit...", self)
        QObject.connect(action, SIGNAL("triggered()"), self.__editSeries)
        self._actions.append(action)
        action = QAction("Delete", self)
        QObject.connect(action, SIGNAL("triggered()"), self.__deleteSeries)
        self._actions.append(action)
        action = QAction("separator", self)
        action.setSeparator(True)
        self._actions.append(action)
        action = QAction("Play", self)
        QObject.connect(action, SIGNAL("triggered()"), self.play)
        self._actions.append(action)
    
    def populateMenu(self, menu):
        assert isinstance(menu, QMenu)        
        menu.addSeparator()
        action = QAction("[series] "+str(self._series.name()), self)
        font = QFont()
        font.setBold(True)
        action.setFont(font)
        menu.addAction(action)
        for item in self._actions:
            menu.addAction(item)

    def play(self):
        assert isinstance(self._series, SeriesNode)
        self.connect(SoundMgr().getWorker(), SIGNAL("soundFinished()"), self.__receipt)
        self.__cpt = 1
        self._series.play()

    def __editSeries(self):        
        dlg = SeriesView(self.parent(), self._series)
        dlg.exec_()

    def __deleteSeries(self):
        self._series.setIsDeleted(True)

    def __receipt(self):
        if(self.__cpt == self._series.repetition()):
            print "OK"
            self.disconnect(SoundMgr().getWorker(), SIGNAL("soundFinished()"), self.__receipt)
            self.emit(SIGNAL("finished()"))
        else:
            self.__cpt += 1
