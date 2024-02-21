class Object():
    tracks = []

    def __init__(self, id, xi,yi,wi,hi,age,timestamp):
        self.Id=id
        self.x=xi
        self.y=yi
        self.w=wi
        self.h=hi
        self.age = age
        self.tracks = []
        self.timestamp = timestamp
        
    def getX(self):
        return  self.x

    def getY(self):
        return  self.y
    def getId(self):
        return  self.Id

    def setAge(self):
        self.age = 0
    def updateCoords(self, xn, yn):
        self.tracks.append([self.x, self.y])
        self.x = xn
        self.y = yn

    def toString(self):
        text = ("Bird ID: " + (str)(self.Id) +
                " ----- Timestamp: " + (str)(self.timestamp) +"\n")
        return text

