from Item import *
from Character import *
from Location import *

class IGame:
    def __init__(self):
        self.mainCharacter = MainCharacter()
        self.location = StartLocation(self)
        self.isRunning = True
    
    def run(self):
        self.isRunning = True
        
        self.onCreate()
        while self.isRunning:
            self.onUpdate()
    
    def onCreate(self):
        pass
        
    def onUpdate(self):
        pass
        