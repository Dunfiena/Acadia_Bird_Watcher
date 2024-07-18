
# Data structure for use in PYQT signal

# We use this to move the two arrays, as well as the percent progress to the cmh_handler.py file
#   while the run is happening.  This keeps the threads from locking, or causing GUI to lock and crash

class signal_DataStruct:
    def __init__(self, progress, birds, birdSave):
        self.data = int(progress)
        self.birds = birds
        self.birdsSave = birdSave

    def getProgress(self):
        return self.data

    def setProgress(self, progress):
        self.data = int(progress)

    def getBirds(self):
        return self.birds

    def setBirds(self, birds):
        self.birdsSave = birds

    def getBirdsSave(self):
        return self.birdsSave

    def setBirdsSave(self, birdSave):
        self.birdsSave = birdSave

    def getStructData(self):
        return self.data, self.birds, self.birdsSave