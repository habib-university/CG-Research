
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


##print(check_255([0,1,0,0]))


