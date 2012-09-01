# -*- coding: utf-8 -*- 

from pygame import mixer

class SoundMgr(object):
    class __SoundMgr():
        def __init__(self):
            self.sounds = {}
            mixer.init()
        def __str__(self):
            return str(self.sounds)
        def add(self, soundName, soundFile):
            self.sounds[soundName] = mixer.Sound(soundFile);
        def play(self, soundName):
            self.sounds[soundName].play()
            while mixer.get_busy():
                pass
    
    instance = None
    
    def __new__(c):
        if not SoundMgr.instance:
            SoundMgr.instance = SoundMgr.__SoundMgr()
        return SoundMgr.instance

    def __getattr__(self, attr):
        return getattr(self.instance, attr)

    def __setattr__(self, attr, val):
        return setattr(self.instance, attr, val)

if __name__ == "__main__":
    x = SoundMgr()
    x.add('anvil', '/usr/lib/openoffice/basis3.2/share/gallery/sounds/ANVIL.WAV')
    x.play('anvil')
    x.play('anvil')
    
