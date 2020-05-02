def BresLineAlgorithm(x0,y0,x1,y1):
    if (abs(y1-y0) < abs(x1-x0)):
        if x0>x1:
            return negLine(x1,y1,x0,y0)
        else:
            return negLine(x0,y0,x1,y1)
    else:
        if y0>y1:
            return posLine(x1,y1,x0,y0)
        else:
            return posLine(x0,y0,x1,y1)

def negLine(x0,y0,x1,y1):
    values = []
    deltaX = x1-x0
    deltaY = y1-y0
    yi = 1
    if deltaY <0:
        yi=-1
        deltaY = deltaY*-1
    D = 2*deltaY - deltaX
    yVal = y0

    for xVal in range(x0,x1):
        values.append([xVal,yVal])
        if D >0:
            yVal = yVal +yi
            D = D -2*deltaX
        D=D+2*deltaY
    values.append([x1,y1])
    return values


def posLine(x0,y0,x1,y1):
    values = []
    deltaX = x1-x0
    deltaY = y1-y0
    xi=1
    if deltaX <0:
        xi = -1
        dx = -dx
    D = 2*deltaX-deltaY
    xVal = x0

    for yVal in range(y0,y1):
        values.append([xVal,yVal])
        if D>0:
            xVal = xVal+xi
            D = D-2*deltaY
        D = D+2*deltaX
    values.append([x1,y1])
    return values
