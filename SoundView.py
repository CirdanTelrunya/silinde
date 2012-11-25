# -*- coding: utf-8 -*- 

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from SoundMgr import SoundMgr
from SoundViewUi import Ui_SoundView

import sys

class SoundView(QDialog):
    def __init__(self, parent=None):
        super(SoundView, self).__init__(parent)
        self.ui = Ui_SoundView()
        self.ui.setupUi(self)
        self.ui.btnFile.setIcon(QIcon.fromTheme("document-open"))
        self.ui.btnAdd.setIcon(QIcon.fromTheme("list-add"))
        self.ui.btnDelete.setIcon(QIcon.fromTheme("list-remove"))        
        self._model = QStringListModel()  
        self.ui.lvwSounds.setModel(self._model)
        self.ui.btnFile.clicked.connect(self._btnFile_clicked)
        self.ui.btnAdd.clicked.connect(self._btnAdd_clicked)
        self.updateModel()

    def updateModel(self):
        sounds = QStringList(SoundMgr().getList())
        self._model.setStringList(sounds)
            

    def _btnFile_clicked(self):
        file = self.ui.ldtFile.text()
        path = ""
        if not file.isEmpty():
            fileinfo = QFileInfo(self.ui.ldtFile.text())
            path = fileinfo.absolutePath()
        fileName = QFileDialog.getOpenFileName(self, "Open sound", QString(path), "Wav Files (*.wav);;All Files (*)")
        
        if fileName.isEmpty() and not file.isEmpty():
            self.ui.ldtFile.setText(file)
        else:
            self.ui.ldtFile.setText(fileName)

    def _btnAdd_clicked(self):
        name = self.ui.ldtName.text()
        file = self.ui.ldtFile.text()
        if name.isEmpty() or file.isEmpty():
            return
        SoundMgr().add(str(name), str(file))
        self.ui.ldtName.clear()
        self.ui.ldtFile.clear()
        self.updateModel()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    SoundMgr().add('kling', '/usr/lib/libreoffice/basis3.3/share/gallery/sounds/kling.wav')
    d = SoundView()
    d.show()
    d.raise_()
    app.exec_()
    SoundMgr.instance = None
