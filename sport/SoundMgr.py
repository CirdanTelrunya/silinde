# -*- coding: utf-8 -*- 

from pygame import mixer
import threading

class SoundMgr(object):
    class __SoundMgr():
        def __init__(self):
            self.sounds = {}
            mixer.init()
        def __del__(self):
            mixer.quit()
            print "delete SoundMgr"
        def __str__(self):
            return str(self.sounds)
        def add(self, soundName, soundFile):
            self.sounds[soundName] = mixer.Sound(soundFile);
        def play(self, soundName):
            self.sounds[soundName].play()
            while mixer.get_busy():
                pass
    
    instance = None
    
    def __new__(self):
        if not SoundMgr.instance:
            SoundMgr.instance = SoundMgr.__SoundMgr()
        return SoundMgr.instance

    def __getattr__(self, attr):
        return getattr(self.instance, attr)

    def __setattr__(self, attr, val):
        return setattr(self.instance, attr, val)

class SoundWorker(threading.Thread):
    def __init__(self, condition, group=None, target=None, name=None, args=(), kwargs={}):
        super(SoundWorker, self).__init__(group, target, name, args, kwargs)
        self._continue = True
        self._condition = condition
        self._sound = None

    def stop(self):
        self._continue = False

    def play(self, sound):
        self._sound = sound

    def run(self):
        self._condition.acquire()
        while True:
            self._condition.wait()
            self._sound.play()
            while mixer.get_busy():
                pass
            print "OK !"
            if not self._continue:
                break            
        self._condition.release()
        pass
        

if __name__ == "__main__":
    condition = threading.Condition()
    worker = SoundWorker(condition)
    worker.start()
    

    x = SoundMgr()
    x.add('anvil', '/usr/lib/openoffice/basis3.2/share/gallery/sounds/ANVIL.WAV')
    x.play('anvil')
    x.play('anvil')
    
    s = mixer.Sound('/usr/lib/openoffice/basis3.2/share/gallery/sounds/ANVIL.WAV')
    
    condition.acquire()
    worker.play(s)
    condition.notify()
    condition.release()

    condition.acquire()
    worker.stop()
    condition.notify()
    condition.release()
    
    SoundMgr.instance = None
