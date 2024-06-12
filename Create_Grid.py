def Generate_Grid(gap = (2,2),H=160,W=128,Origin = (80,64),Pos = (0,0),Zoom = 1):
    if type(gap) == type(0):
        gap = (gap,gap)
    x_points = []
    y_points = []
    for x in range(H):
        x-=Origin[0]
        x = x*Zoom
        if x%gap[0] == 1:
            x_points.append(x)
    for y in range(W):
        y-=Origin[1]
        y = y*Zoom
        if y%gap[1] == 1:
            y_points.append(y)
    return [x_points,y_points]

def Blend_Lists(x,y = None):
    if y == None:
        x,y,*extra = x
    shortest = min((len(x),len(y)))
    out = []
    for i in range(shortest):
        out.append([x[i],y[i]])
    return out,extra