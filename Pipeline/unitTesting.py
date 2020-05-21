from bressenham import *
from primitiveClass import *
def checkBresenham():
    print(BresLineAlgorithm(20,10,30,18))
#checkBresenham()

def checkLineFunctions():
    ##line=Line()
    ##line.GL_LINES([[1,1],[2,2],[3,3],[4,4]])
    ##line.printLines()
    ##lineodd=Line()
    ##lineodd.GL_LINES([[1,1],[2,2],[3,3],[4,4],[5,5]])
    ##lineodd.printLines()
    ##linestrip=Line()
    ##linestrip.GL_LINE_STRIP([[1,1],[2,2],[3,3],[4,4],[5,5],[6,6]])
    ##linestrip.printLines()
    lineloop=Line()
    lineloop.GL_LINE_LOOP([[1,1],[2,2],[3,3],[4,4],[5,5],[6,6]])
    lineloop.printLines()

def checkClockwise():
    tri = Triangle()
    #print(tri.clockwiseFace([5,5],[0,0],[5,0]))
    vertices = [[1,10],[0,8],[3,10],[2,7],[5,8],[3,5],[6,6],[5,3],[7,4]]
    #tri.GL_TRIANGLES(vertices)
    #tri.printTriArray()
    tri.GL_TRIANGLE_STRIP(vertices)
    tri.printTriArray()
    #tri.GL_TRIANGLE_FAN(vertices)
    #tri.printTriArray()
checkClockwise()
