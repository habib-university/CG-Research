def convert_01(val):
    temp = []
    for i in range(len(val)):
        temp.append(round(val[i]/255, 5))
    return temp
    
def convert_255(val):
    temp = []
    for i in range(len(val)):
        temp.append(round(val[i] * 255, 1))
    return temp

def check_255(v):
    val = v.copy()
    for i in range(len(val)):
        if val[i] >= 0 and val[i] <= 1:
            continue
        elif val[i] >= 0 and val[i] <= 255:
            return True
    return False

def coordinate_conversion(x,y, block_size, margin):
    new_coord = [margin, margin]
    if x != 0 or y != 0:
        new_coord[0] += ((block_size + margin) * x)
        new_coord[1] += ((block_size + margin) * y)
    return new_coord

def screen_resolution(width, height, block_size = 20, margin = 5):
    w = (width * block_size) + (width * margin) + margin
    h = (height * block_size) + (height * margin) + margin
    return w, h, block_size, margin


