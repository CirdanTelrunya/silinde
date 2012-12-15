#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PlaylistUi import Ui_Playlist
import sys
from SoundMgr import SoundMgr

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

class Iterator(object):
    def __init__(self, playlist):
        assert isinstance(playlist, Playlist)
        self._playlist = playlist
        self._current_desc = 0
        self._current_sound = 0

    def __iter__(self):
        return self

    def next(self):
        if self._current_desc < len(self._playlist._list):
            desc, sounds = self._playlist._list[self._current_desc]
            sound = None
            if self._current_sound < len(sounds):                
                self._current_sound += 1
                sound = sounds[self._current_sound - 1]
            else:
                self._current_sound = 0
                self._current_desc += 1

            return desc, sound
        else:
            raise StopIteration

class PlaylistView(QDialog):
    def __init__(self, playlist, parent=None):
        super(PlaylistView, self).__init__(parent)
        assert isinstance(playlist, Playlist)
        self._playlist = playlist
        self._current = Iterator(playlist)
        self._continue = False

        size = 0
        for i in Iterator(playlist):
            size += 1

        self.ctimer = QTimer()
        self.ctimer.setSingleShot(True)
        self.ui = Ui_Playlist()
        self.ui.setupUi(self)
        
        self.ui.btnQuit.setIcon(QIcon.fromTheme("media-playback-stop"))
        self.ui.btnPlayPause.toggled.connect(self._btnPlayPause_toggled)
        self.ui.iconStart = QIcon.fromTheme("media-playback-start")
        self.ui.iconPause = QIcon.fromTheme("media-playback-pause")
        self.ui.btnPlayPause.setIcon(self.ui.iconStart)
        self.ui.pbrSession.setMinimum(0)
        self.ui.pbrSession.setMaximum(size)
        self.ui.pbrSession.setValue(0)
        self.ctimer.timeout.connect(self._play)


    def _btnPlayPause_toggled(self, toggle):
        if(toggle):
            if(self.ui.pbrSession.value() == self.ui.pbrSession.maximum()):
                self.ui.pbrSession.setValue(0)

            self.ui.btnPlayPause.setIcon(self.ui.iconPause)
            self._continue = True
            self.ctimer.start(1000)
        else:
            self.ui.btnPlayPause.setIcon(self.ui.iconStart)
            self._continue = False
            
    def _play(self):
        if(self._continue):
            try:
                desc, sound = self._current.next()
                print str(desc)+" "+str(sound)
                self.ui.pbrSession.setValue(self.ui.pbrSession.value()+1)
                self.ctimer.start(1000)
            except StopIteration:
                self._current = Iterator(playlist)
                self.ui.btnPlayPause.toggle()
                pass
        pass
    

if __name__ == "__main__":
    playlist = Playlist()
    for j in xrange(1, 3):
        desc = DescriptionItem()
        desc.description = "Hop" + str(j)
        plop = []
        for i in xrange(1, 2):
            s = SoundItem()
            s.sound = "sound_" + str(i)
            plop.append(s)
        playlist.append(desc, plop)

    app = QApplication(sys.argv)
    # SoundMgr().add('kling', '/usr/lib/libreoffice/basis3.3/share/gallery/sounds/kling.wav')
    d = PlaylistView(playlist)
    d.show()
    d.raise_()
    app.exec_()
    # SoundMgr.instance = None
    


    # iter = Iterator(playlist)
    # try:
    #     while 1:
    #         desc, sound = iter.next()
    #         print str(desc)+" "+str(sound)
    # except StopIteration:
    #     pass

    
