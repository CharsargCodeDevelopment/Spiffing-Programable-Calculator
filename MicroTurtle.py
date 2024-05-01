import DisplaySystem as DispSys

global pos

__draw__ = True
__width__ = 2
__color__ = (0,0,0)
pos = (0,0)
def width(width):
    __width__ = width
def penup():
    __draw__ = False
def pendown():
    __draw__ = True
def goto(x,y=None):
    global pos
    if y == None:
        x,y = x
    if __draw__:
        draw(pos,(x,y))
    pos = (x,y)
    
def draw(start,end):
    x1,y1 = start
    x2,y2 = end
    x_plot = []
    y_plot = []
    r,g,b = __color__
    for x in range(x1,x2):
        y = y1 + (((x-x1)*(y2-y1))/(x2-x1))
        DispSys.SetPixel(x,y,r,g,b,1)
        x_plot.append(x)
        y_plot.append(y)
    print(x_plot)
    #r,g,b = __color__
    #DispSys.SetPixel(x,y)
    DispSys.Plot(x_plot,y_plot,r,g,b)
def color(r,g=None,b=None):
    if g==None or b == None:
        r,g,b = r
    __color__ = (r,g,b)
    
class Turtle():
    def __init__():
        penup = staticmethod(penup)
        pendown = staticmethod(pendown)
        goto = staticmethod(goto)
    
for x in range(-60,60):
    DispSys.SetPixel(x,10,0,0,0)
    goto(x,5)

for x in range(-80,80):
    for y in range(-64,64):
        DispSys.SetPixel(x,y,255,0,0)