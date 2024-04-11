from Bird import Object

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