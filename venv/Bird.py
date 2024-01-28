class Object():
    tracks = []

    def __init__(self, id, xi,yi,wi,hi):
        self.Id=id
        self.x=xi
        self.y=yi
        self.w=wi
        self.h=hi
        self.age=0
        self.max_age = 5
        self.tracks = []
        
    def getX(self):
        return  self.x

    def getY(self):
        return  self.y
    def getId(self):
        return  self.Id

    def updateCoords(self, xn, yn):
        self.tracks.append([self.x, self.y])
        self.x =xn
        self.y=yn

