class Point:
    def __init__(self):
        #By default it is 1, and needs to be enabled
        self.pointSize= 1
        
class Line:
    def __init__(self):
##        self.x0
##        self.y0
##        self.x1
##        self.y1
        self.lineArray = []
    def GL_LINES(self,vertices):
        if (len(vertices)%2==0):
            for i in range(0,len(vertices),2):
                self.lineArray.append([vertices[i],vertices[i+1]])
        else:
            for i in range(0,len(vertices)-1,2):
                self.lineArray.append([vertices[i],vertices[i+1]])
    def GL_LINE_STRIP(self,vertices):
        for i in range(0,len(vertices)):
            if (i!=len(vertices)-1):
                self.lineArray.append([vertices[i],vertices[i+1]])
    def GL_LINE_LOOP(self,vertices):
        for i in range(0,len(vertices)):
            if (i!=len(vertices)-1):
                self.lineArray.append([vertices[i],vertices[i+1]])            
            else:
                self.lineArray.append([vertices[i],vertices[0]])

    def printLines(self):
        print(self.lineArray)



