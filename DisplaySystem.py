# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text.
"""

import board
import terminalio
import displayio
import adafruit_display_shapes as drawshapes
import busio
#import fourwire
from adafruit_display_text import label
from adafruit_display_text.scrolling_label import ScrollingLabel
from adafruit_st7735r import ST7735R
import Line as BLine
import framebufferio
from time import time,sleep
import bitmaptools
# Release any resources currently in use for the displays
displayio.release_displays()

#spi = busio.SPI()
tft_cs = board.GP21
tft_dc = board.GP22

spi = busio.SPI(board.GP26,board.GP27,board.GP28)
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.GP20)

display = ST7735R(display_bus, width=160, height=128, rotation=90, bgr=True,auto_refresh=False)

#import InputSystem

# Make the display context
image = displayio.Group()
display.root_group = image


##BackGround
Back_bitmap = displayio.Bitmap(160, 128, 1)
color_palette = displayio.Palette(1)
#print(color_palette)
color_palette[0] = (255,255,255)  # Bright Green

bg_sprite = displayio.TileGrid(Back_bitmap, pixel_shader=color_palette, x=0, y=0)
image.append(bg_sprite)

RGB_Index_Table = {}

#Image
img_bitmap = displayio.Bitmap(160, 128, 64)
rgb_range = (4,4,4)
colors = rgb_range[0]*rgb_range[1]*rgb_range[2]*2
img_palette = displayio.Palette(colors)
i = 0
for r in range(rgb_range[0]):
    for b in range(rgb_range[2]):
        for g in range(rgb_range[1]):
            for a in range(2):
                r1 = int(255*(r/rgb_range[0]))
                g1 = int(255*(g/rgb_range[1]))
                b1 = int(255*(b/rgb_range[2]))
                #print(r1,g1,b1,a)
                img_palette[i] = (r1,g1,b1)
                if a == 0:
                    img_palette.make_transparent(i)
                RGB_Index_Table[(r,g,b,a)] = i
                i+=1
#input()
#img_palette = displayio.Palette(1)
#img_palette[0] = (255,255,255)  # Bright Green

img_sprite = displayio.TileGrid(img_bitmap, pixel_shader=img_palette, x=0, y=0)
image.append(img_sprite)

def Convert_To_6Bit(r,g,b):
    DivideBy256 = 1/256
    r1 = int(4*(r*DivideBy256))
    g1 = int(4*(g*DivideBy256))
    b1 = int(4*(b*DivideBy256))
    return (r1,g1,b1)
def Covert_6Bit_To_I(r,g=None,b=None,a=1):
    if type(r) == type([]) or type(r) == type(()):
        g = r[1]
        b = r[2]
        r = r[0]
        #print(r,g,b)
    #print(RGB_Index_Table[(r,g,b,a)])
    return RGB_Index_Table[(r,g,b,a)]

def SetPixel(x,y,r,g,b,a=1,center = (80,64)):
    x+=center[0]
    y+=center[1]
    r,g,b = Convert_To_6Bit(r,g,b)
    i = Covert_6Bit_To_I(r,g,b,a)
    if int(x) < 0:
        return
    if int(y) < 0:
        return
    if int(x) > 159:
        return
    if int(y) > 127:
        return
    img_bitmap[int(x),int(y)] = i
def Clear():
    #print(H)
    for x in range(H):
        for y in range(W):
            img_bitmap[x, y] = 0

def Plot(x,y,r=255,g=0,b=0):
    if len(x) != len(y):
        print("Length mishmatch: The list lengths are not equal, {0}({1})!={2}({3})".format(len(x),"x",len(y),"y"))
    for i in range(min(len(x),len(y))):
        X = x[i]
        Y = y[i]
        #print(X,Y)
        SetPixel(X,Y,r,g,b)




"""
# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(150, 118, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0xAA0088  # Purple
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=5)
splash.append(inner_sprite)
"""
"""
# Draw a label
text_group = displayio.Group(scale=2, x=11, y=64)
text = "Hello World!"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
text_group.append(text_area)  # Subgroup for text scaling
image.append(text_group)
"""
def Line(start,end,r=255,g=0,b=0,last_points = []):
    x1,y1 = start
    x2,y2 = end
    x_plot = []
    y_plot = []
    points = BLine.Calc_Line(start,end)
    for point in points:
        if point in last_points:
            continue
        x,y = point
        x += 80
        y += 64
        if x > 159:
            pass
        elif y > 127:
            pass
        elif x < 0:
            pass
        elif y < 0:
            pass
        else:
            x -= 80
            y -= 64
            x_plot.append(x)
            y_plot.append(y)
    Plot(x_plot,y_plot,r,g,b)
    output = []
    while not (len(x_plot) == 0 or len(y_plot) == 0):
        x = x_plot.pop(0)
        y = y_plot.pop(0)
        if (x,y) in output:
            print("GONE")
            continue
        output.append((x,y))
    return points

def DrawNativeLine(start,end,Color = 5,last_points = []):
    x1, y1 = start
    x2, y2 = end
    SetPixel(x1,y1,r,g,b)
    bitmaptools.draw_line(img_bitmap,x1+80,y1+64,x2+80,y2+64,Color)
    #drawshapes.line.Line(('{:02x}{:02x}{:02x}'.format(r,g,b)).upper())

def RenderGraph(pos=(0,0),zoom = 1,last_points = []):
    Clear()
        #print(time()-start,frames,fps,j)
    totalStart = time()
    points = []
    #zoom = float(input())
    #pos = (j,0)
    Grid = grid.Generate_Grid(gap=20)
    r6,g6,b6 = Convert_To_6Bit(0,0,0)
    RGBI =Covert_6Bit_To_I(r6,g6,b6)
    for x in Grid[0]:
        y1 = int(W*0.5)
        y2 = -y1
        DrawNativeLine((x,y1),(x,y2),RGBI)
    for y in Grid[1]:
        x1 = int(H*0.5)
        x2 = -x1
        #print(y)
        DrawNativeLine((x1,y),(x2,y),RGBI)
    """
    for x in Grid[0]:
        y = []
        for i in range(W):
            y.append(i-64)
        del i
        x = [x]*W
        Plot(x,y,r=0,g=0,b=0)
    for y in Grid[1]:
        x = []
        for i in range(H):
            x.append(i-80)
            #print(i-80)
            #print(max(x),min(x))
        del i
        y = [y]*H
        Plot(x,y,r=0,g=0,b=0)
    """
    #last_points = last_points.copy()
    """
    print(Grid)
    i=0
    for _ in last_points:
        x,y = last_points[i]
        if x in Grid[0] or y in Grid[1]:
            i += 1
            continue
        last_points.pop(i)
            
    """
    #display.refresh()
    Start = time()
    print(time()-totalStart)
    Data = RunGraph.ProscsessGraph(calculations,variables,H,W,XRange,YRange,pos = pos,res = 1,zoom=zoom)
    if Data[0] == None:
        print(Data[1])
        return Data
    End = time()
    print(End-Start)
    #print(Data)
    pos = None
    LINE_DATA = []
    #for line in Data:
     #   image.append(Polygon(zip(line[0],line[1]),outline = 0x0000FF,close=False))
        
    #display.refresh()
    for line in Data:
        line_points = []
        X = line[0]
        Y = line[1]
        R,G,B = line[2]
        r6,g6,b6 = Convert_To_6Bit(R,G,B)
        RGBI =Covert_6Bit_To_I(r6,g6,b6)
        pos = None
        for i in range(min(len(X),len(Y))):
            x = X[i]
            y = Y[i]
            if pos != None:
                #display.refresh()
                #print(len(points))
                #print("StrtingLine")
                THELINE = (DrawNativeLine(pos,(x,y),RGBI,last_points=last_points))
                #print("DoneLine")
                #points.extend(THELINE)
                #line_points.extend(THELINE)
                del THELINE
            pos = (x,y)
        LINE_DATA.append(line_points)
            #pos = (x,y)
    print("StartSettingPixels")
    """
    i = 0
    print(len(last_points))
    for _ in range(len(last_points)):
        last_point = last_points[i]
        if last_point in points:
            last_points.pop(i)
        else:
            i+=1
    print(time()-Start)
    for last_point in last_points:
        x,y = last_point
        SetPixel(x,y,255,255,255,0)
    print(time()-Start)
    print("EndSettingPxiels")
    """
    display.refresh()
    return points,LINE_DATA

import RunGraph
import Create_Grid as grid
#import AudioOut as AO
import ReadKeypad as InputSystem
import Line as BLine
import UserInterFaceSystem
calculations = [["y=x",(0,255,0)],["y=sin(x)*5",(0,0,255)]]
variables = {}
H = 160
W = 128
XRange = 16
YRange = 12
points = {}
j=0
last_points = []
Dir = True
display.refresh()
start = time()
frames = 0
fps = 0
zoom = 1
__PROCESSESES__ = ["RENDER GRAPH","PLAY GRAPH","GET INPUT","FUNCTIONS"]
__HearGraphLine__ = {0:0,1:1}
__GraphSoundLower__ = 440
__GraphSoundUpper__ = 880
__GraphSoundDelta__ = __GraphSoundUpper__ - __GraphSoundLower__
__GraphSoundMultiplier__ = __GraphSoundDelta__/H
PROCESSES = ""
ButtonAssignments = {(0,0):"Home",(1,0):"Configure Graph",(3,1):"1",(4,1):"2",(5,1):"3",(3,2):"4",(4,2):"5",(5,2):"6",(3,3):"7",(4,3):"8",(5,3):"9",(0,2):"LEFT",(1,1):"UP",(2,2):"RIGHT",(5,0):"SHIFT"}
while True:
    pressed = []
    #print(display.auto_refresh)
    if frames >= 10:
        frames = 0
        start = time()
    DeltaTime = time()-start
    if DeltaTime !=0:
        fps = frames/DeltaTime
    for PROCESSES in __PROCESSESES__:
        #print(__PROCESSESES__)
        if PROCESSES == "RENDER GRAPH":
            RenderGraphOutPut = RenderGraph(pos=(j/2,0),zoom=1,last_points=last_points)
            if RenderGraphOutPut[0] != None:
                points,Line_Points = RenderGraphOutPut
            else:
                print("ERROR:")
                error = (RenderGraphOutPut)
                error.pop(0)
                print(error)
                Error_Text = """
ERROR!!!!
CULPRIT EQUATION:
{0}
""".format(error[1])
                #text_group = displayio.Group(scale=2, x=11, y=64)
                #text = "Hello World!"
                #text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
                #text_group.append(text_area)  # Subgroup for text scaling
                #image.append(text_group)
                Error_Group = displayio.Group(scale=1, x=10, y=10)
                Error = label.Label(terminalio.FONT, text=Error_Text, color=0xFF0000)
                Error_Group.append(Error)
                image.append(Error_Group)
                
                display.refresh()
                #input()
        elif PROCESSES == "PLAY GRAPH":
            continue
            print('Starting Sound')
            #AO.Set_Amplitude(1)
            for i in range(len(Line_Points[0])):
                for Pin in __HearGraphLine__:
                    pos = Line_Points[__HearGraphLine__[Pin]][i]
                    AO.Set_Amplitude(1,Pin)
                    #SetPixel(x,y,255,0,255,1)
                    x,y = pos
                    #SetPixel(x,y,255,0,255,0)
                    y += H/2
                    htz = int((y*__GraphSoundMultiplier__)+__GraphSoundLower__)
                    #print(htz,y)
                    AO.buzzer[Pin].frequency = htz
                    #SetPixel(x,y-H/2,255,0,255,1)
                    sleep(0.005)
            for Pin in __HearGraphLine__:
                AO.Set_Amplitude(0,Pin)
            print('Stopped Sound')
        elif PROCESSES=="GET INPUT":
            PressedPoses = InputSystem.ReadPins()
            print(PressedPoses)
            PressedPoses = InputSystem.ReassignPins(PressedPoses,InputSystem.__ReasignmentIndex__)
            print(PressedPoses)
            pressed = []
            for pos in PressedPoses:
                if pos in ButtonAssignments:
                    pressed.append(ButtonAssignments[pos])
                else:
                    pressed.append(pos)
            print(pressed)
            if "PROSCESS INPUT" in __PROCESSESES__:
                __PROCESSESES__.remove("PROSCESS INPUT")
            if len(pressed) > 0:
                __PROCESSESES__.append("PROSCESS INPUT")
        elif PROCESSES == "PROSCESS INPUT":
            for button in pressed:
                if "GRAPH CONFIGURE" in __PROCESSESES__:
                    __PROCESSESES__.remove("GRAPH CONFIGURE")
                if button == "Configure Graph":
                    __PROCESSESES__.append("GRAPH CONFIGURE")
        elif PROCESSES == "GRAPH CONFIGURE":
            print(calculations)
            calculations = UserInterFaceSystem.UI(display)
            print(calculations)
            display.root_group = image
            __PROCESSESES__.remove("GRAPH CONFIGURE")
    #print(Line_Points[__HearGraphLine__])
    
        #print(time()-start,frames,fps,
    last_points = points
    frames +=1
    j+=1