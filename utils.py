def hitung_range(OldMax, OldMin, NewMax, NewMin, OldValue):
    OldRange = (OldMax - OldMin)  
    NewRange = (NewMax - NewMin)  
    NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
    return NewValue

def midpoint(x1,y1,x2,y2):
    x_mid = (x1 + x2)/2
    y_mid = (y1 + y2)/2
    return int(x_mid),int(y_mid)