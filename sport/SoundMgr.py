# -*- coding: utf-8 -*- 

from PyQt4.QtCore import *
from PyQt4 import QtGui
from pygame import mixer
from time import sleep
import threading
import sys

class SoundMgr(object):
    class __SoundMgr():
        def __init__(self):
            self.sounds = {}
            mixer.init()
            self._queue = SharedQueue()
            self._worker = QSoundWorker(queue = self._queue)
            self._worker.start()
            
        def getWorker(self):
            return self._worker

        def __del__(self):
            self._worker.stop()
            self._queue.put(None)
            self._worker.wait()
            mixer.quit()
            print "delete SoundMgr"

        def __str__(self):
            return str(self.sounds)
        def add(self, soundName, soundFile):
            self.sounds[soundName] = mixer.Sound(soundFile);

        def play(self, soundName, startTime = 0):
            item = SoundItem(self.sounds[soundName], startTime)
            self._queue.put(item);    
    instance = None
    
    def __new__(self):
        if not SoundMgr.instance:
            SoundMgr.instance = SoundMgr.__SoundMgr()
        return SoundMgr.instance

    def __getattr__(self, attr):
        return getattr(self.instance, attr)

    def __setattr__(self, attr, val):
        return setattr(self.instance, attr, val)

class SoundItem(object):
    def __init__(self, sound, startTime = 0):
        assert isinstance(sound, mixer.Sound)
        self.sound = sound
        self.startTime = startTime

class QSoundWorker(QThread):
    def __init__(self, parent = None, queue = None):
        QThread.__init__(self, parent)
        self._continue = True
        assert isinstance(queue, SharedQueue)
        self._queue = queue
        self._mutex = QMutex()
        
    def stop(self):
        self._mutex.lock()
        self._continue = False
        self._mutex.unlock()

    def run(self):
        while self._continue:
            item = self._queue.get()
            if item is not None:
                assert isinstance(item, SoundItem)
                sleep(item.startTime)
                item.sound.play()
                while mixer.get_busy():
                    pass
                self.emit(SIGNAL("soundFinished()"))
        pass

class SharedQueue(object):
    def __init__(self):
        self._queue = []
        self._mutex = QMutex()
        self._condition = QWaitCondition()

    def size(self):
        self._mutex.lock();
        size = len(self._queue)
        self._mutex.unlock();
        return size

    def put(self, item):
        self._mutex.lock();
        self._queue.append(item)
        self._condition.wakeAll();
        self._mutex.unlock();
        pass

    def get(self):
        self._mutex.lock();
        if len(self._queue) == 0:
            self._condition.wait(self._mutex);
        item = self._queue.pop()
        self._mutex.unlock();
        return item
        pass


class TerminalViewer(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        # self.Label = QtGui.QLabel("Waiting for Something",self)
        self.button = QtGui.QPushButton("OK", self)
        self.connect(self.button,SIGNAL("clicked ( ) "), self.Activated)
        x = SoundMgr()
        x.add('kling', '/usr/lib/libreoffice/basis3.3/share/gallery/sounds/kling.wav')
        self.connect(x.getWorker(), SIGNAL("soundFinished()"), self.receipt)
        
    def Activated(self):
        print "OK"
        SoundMgr().play('kling')
                
    def closeEvent(self,e):
        SoundMgr.instance = None
        e.accept()
        app.exit()

    def receipt(self):
        print "Sound OK"


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    qb = TerminalViewer()
    qb.show()
    sys.exit(app.exec_())
    


# if __name__ == "__main__":
#     condition = threading.Condition()
#     worker = SoundWorker(condition)
#     worker.start()
    

#     x = SoundMgr()
#     x.add('anvil', '/usr/lib/openoffice/basis3.2/share/gallery/sounds/ANVIL.WAV')
#     x.play('anvil')
#     x.play('anvil')
    
#     s = mixer.Sound('/usr/lib/openoffice/basis3.2/share/gallery/sounds/ANVIL.WAV')
    
#     condition.acquire()
#     worker.play(s)
#     condition.notify()
#     condition.release()

#     condition.acquire()
#     worker.stop()
#     condition.notify()
#     condition.release()
    
#     SoundMgr.instance = None
