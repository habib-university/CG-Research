class Point:
    def __init__(self,xVal,yVal):
        self.x = xVal
        self.y = yVal
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


class Triangle:
    def __init__(self):
        self.triangleArray = []
    def GL_TRIANGLES(self,vertices):
        if (len(vertices)>2):
            if (len(vertices)%3!=0):
                print("Not enough values, last",len(vertices)%3,"value(s) popped")
                for i in range(0,len(vertices)%3):
                    vertices.pop(-1)
            for i in range(0,len(vertices),3):
                self.triangleArray.append([[vertices[i]],[vertices[i+1]],[vertices[i+2]]])
        else:
            print("Not enough values")
        
    def GL_TRIANGLE_STRIP(self, vertices):        
        #Checking if the first face is clockwise or anticlockwise
        if (len(vertices)>2):
            faceDirection = self.clockwiseFace(vertices[0],vertices[1],vertices[2])
            for i in range(0,len(vertices)-2):
                if (self.clockwiseFace(vertices[i],vertices[i+1],vertices[i+2]) == faceDirection):
                    self.triangleArray.append([[vertices[i]],[vertices[i+1]],[vertices[i+2]]])
                else:
                    self.triangleArray.append([[vertices[i+1]],[vertices[i]],[vertices[i+2]]])
        else:
            print("Not enough values")
    def GL_TRIANGLE_FAN(self,vertices):
        if (len(vertices)>2):
            for i in range(1,len(vertices)-1,1):
                self.triangleArray.append([vertices[0],vertices[i],vertices[i+1]])
        else:
            print("Not enough values")
    def printTriArray(self):
        for i in range(0,len(self.triangleArray)):
            print(self.triangleArray[i])
            
    def clockwiseFace(self,a,b,c):
        #AntiClockWise
        if (b[0] - a[0])*(c[1]-a[1])-(c[0]-a[0])*(b[1]-a[1])> 0:
            return "Counterclockwise"
        #Clockwise
        elif (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])<0:
            return "Clockwise"
        else:
            return "Linear"
        
