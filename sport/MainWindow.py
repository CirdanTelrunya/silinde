#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from MainWindowUi import Ui_MainWindow
import sys
from Training import TrainingNode
from treenode.TreeNodeItemModel import TreeNodeItemModel
from SoundMgr import SoundMgr
import pickle
import icons

class MainWindow(QMainWindow):
    def __init__ (self, parent = None, flags = 0):
        super(MainWindow, self).__init__(parent, Qt.WindowFlags(flags))
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        root = TrainingNode('training')
        model = TreeNodeItemModel(root)
        tv = self.ui.treeView
        tv.setModel(model)
        QObject.connect(self.ui.actionLoad, SIGNAL("triggered()"), self.load)
        QObject.connect(self.ui.actionSave, SIGNAL("triggered()"), self.save)
        
    def load(self):
        fileName = QFileDialog.getOpenFileName(self, "Open training", QString(), "Plk Files (*.plk);;All Files (*)")
        input = open(fileName, 'rb')
        root = pickle.load(input)
        model = TreeNodeItemModel(root)
        self.ui.treeView.setModel(model)
        print 'load'

    def save(self):
        fileName = QFileDialog.getSaveFileName(self, "Save training", QString(), "Plk Files (*.plk);;All Files (*)")
        output = open(fileName, 'wb')
        root = self.ui.treeView.getRootNode()
        pickle.dump(root, output)
        print 'save'
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    soundMgr = SoundMgr()
    # soundMgr.add('kling', '/usr/lib/libreoffice/basis3.3/share/gallery/sounds/kling.wav')
    soundMgr.add('kling', '/usr/lib/openoffice/basis3.2/share/gallery/sounds/kling.wav')
    soundMgr.add('anvil', '/usr/lib/openoffice/basis3.2/share/gallery/sounds/ANVIL.WAV')
    
    main = MainWindow()
    main.show()
    app.exec_()
    SoundMgr.instance = None
    sys.exit()
    
