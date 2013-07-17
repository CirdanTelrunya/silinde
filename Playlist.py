#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PlaylistUi import Ui_Playlist
import sys
from SoundMgr import SoundMgr
import itertools

class DescriptionItem(object):
    def __init__ (self):
        self.description = None
        self.image = None
        pass
    def __str__(self):
        return str(self.description)
    
class SoundItem(object):
    def __init__ (self):
        self.delay = None
        self.sound = None
        pass
    def __str__(self):
        return str(self.sound)
    
class Playlist(object):
    def __init__ (self):
        self._list = []
        pass

    def append(self, description, sounds):
        assert isinstance(sounds, list)        
        self._list.append((description, sounds))
        pass

    def play(self):
        for desc, sounds in self._list:
            print str(desc)
            for sound in sounds:
                assert isinstance(sound, SoundItem)
                print str(sound)
    
    def generator(self):
        for desc, sounds in self._list:
            # yield desc
            for sound in sounds:
                assert isinstance(sound, SoundItem)
                yield desc, sound

    def nbTotalSounds(self):
        sum = 0
        for desc, sounds in self._list:
            sum = sum + len(sounds)
        return sum

class PlaylistView(QDialog):
    def __init__(self, playlist, parent=None):
        super(PlaylistView, self).__init__(parent)
        assert isinstance(playlist, Playlist)
        self._playlist = playlist
        self._current = None
        self._continue = False
        self._waiting = False
        self.ui = Ui_Playlist()
        self.ui.setupUi(self)
        
        self.ui.btnQuit.setIcon(QIcon.fromTheme("media-playback-stop"))
        self.ui.btnPlayPause.toggled.connect(self._btnPlayPause_toggled)
        self.ui.iconStart = QIcon.fromTheme("media-playback-start")
        self.ui.iconPause = QIcon.fromTheme("media-playback-pause")
        self.ui.btnPlayPause.setIcon(self.ui.iconStart)
        self.ui.pbrSession.setMinimum(0)
        self.ui.pbrSession.setMaximum(playlist.nbTotalSounds())
        self.ui.pbrSession.setValue(0)

    def _btnPlayPause_toggled(self, toggle):
        if(toggle):
            if(self.ui.pbrSession.value() == self.ui.pbrSession.maximum()):
                self.ui.pbrSession.setValue(0)
            
            self.ui.btnPlayPause.setIcon(self.ui.iconPause)
            self._continue = True
            self.connect(SoundMgr().getWorker(), SIGNAL("soundFinished()"), self._play)
            self._play()
        else:
            self.ui.btnPlayPause.setIcon(self.ui.iconStart)
            self._continue = False
            if self._waiting:                
                self.disconnect(SoundMgr().getWorker(), SIGNAL("soundFinished()"), self._play)
                self.connect(SoundMgr().getWorker(), SIGNAL("soundFinished()"), self._wait)                
                self.ui.btnPlayPause.setEnabled(False)

    def _wait(self):
        self.ui.btnPlayPause.setEnabled(True)
        self.ui.pbrSession.setValue(self.ui.pbrSession.value()+1)
        self._waiting = False
            
    def _play(self):
        if(self._continue):
            if self._current == None:
                self._current = self._playlist.generator()
            if self._waiting:
                self.ui.pbrSession.setValue(self.ui.pbrSession.value()+1)
            try:
                desc, sound = self._current.next()
                SoundMgr().play(sound.sound, sound.delay)
                self._waiting = True
                # print str(desc)+" "+str(sound)
                print type(desc)
                self.ui.tdtDescription.setPlainText(QString(desc.description))
            except StopIteration:
                self._current = None
                self._waiting = False
                self.ui.btnPlayPause.toggle()
                self.disconnect(SoundMgr().getWorker(), SIGNAL("soundFinished()"), self._play)
                self.ui.pbrSession.setValue(self.ui.pbrSession.value()+1)
                pass
        pass
    

if __name__ == "__main__":
    playlist = Playlist()
    for j in xrange(1, 3):
        desc = DescriptionItem()
        desc.description = "Hop" + str(j)
        plop = []
        for i in xrange(0, 2):
            s = SoundItem()
            s.sound = 'anvil'
            s.delay = 10
            plop.append(s)
        playlist.append(desc, plop)

    app = QApplication(sys.argv)
    # SoundMgr().add('kling', '/usr/lib/openoffice/basis3.2/share/gallery/sounds/kling.wav')
    SoundMgr().add('anvil', '/usr/lib/openoffice/basis3.2/share/gallery/sounds/ANVIL.WAV')
    # SoundMgr().add('kling', '/usr/lib/libreoffice/basis3.3/share/gallery/sounds/kling.wav')
    d = PlaylistView(playlist)
    d.show()
    d.raise_()
    app.exec_()
    SoundMgr.instance = None
    
