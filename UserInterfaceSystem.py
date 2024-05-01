import board
import terminalio
import displayio
import busio
#import fourwire
from adafruit_display_text import label
from adafruit_st7735r import ST7735R
import Line as BLine
import framebufferio
from time import time,sleep
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_text import bitmap_label
from adafruit_bitmap_font import bitmap_font
import terminalio
import bitmaptools
import ReadKeypad

ButtonAssignments = {(0,0):"Home",(1,0):"Configure Graph",(3,1):"1",(4,1):"2",(5,1):"3",(3,2):"4",(4,2):"5",(5,2):"6",(3,3):"7",(4,3):"8",(5,3):"9",(0,2):"<-",(1,1):">>",(2,2):"->",(1,2):"<<",(5,0):"SHIFT"}

def UI(display):

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

    display.refresh()

    Outline = Rect(0, 0, 160, 127, fill=0xffffff, outline=0x000000, stroke=5)
    TopBox = Rect(0, 28, 160, 127, fill=0xffffff, outline=0x000000, stroke=5)
    BottomBox = Rect(0, 82, 160, 127, fill=0xffffff, outline=0x000000, stroke=5)

    image.append(Outline)
    image.append(TopBox)
    image.append(BottomBox)

    display.refresh()


    Calculations = [['y=x', (0, 255, 0)], ['y=sin(x)*5', (0, 0, 255)]]


    Calc_Num = 1
    Total_Calc = 1
    Calculation = Calculations[Calc_Num-1]

    CalcIndex = label.Label(terminalio.FONT, text="{0}/{1}".format(Calc_Num,Total_Calc), color=0x000000)
    CalcIndex.x = 7
    CalcIndex.y = 14

    Equation = label.Label(terminalio.FONT, text=Calculation[0], color=0x000000)
    print(Equation.scale)
    Equation.x = 7
    Equation.y = 55

    image.append(CalcIndex)
    CalcIndexIndex = len(image)-1
    image.append(Equation)
    Equation_Index = len(image)-1
    #display.root_group = Equation
    #image.append(Equation)
    display.refresh()

    cursor = len(list(Calculation))


    font = bitmap_font.load_font("/FONTS/cursor.bdf")
    CursorSymb = label.Label(text=(" "*(cursor-1))+"I", color=0x000000,font = font)
    CursorSymb.x = 10
    CursorSymb.y = 55

    image.append(CursorSymb)

    Cursor_Index = len(image)-1

    display.refresh()
    UIRunning = True
    pressed = []
    while UIRunning:
        
        Total_Calc = len(Calculations)
        Calculation = Calculations[Calc_Num-1][0]
        PressedPins = ReadKeypad.ReadPins()
        PressedPoses = ReadKeypad.ReassignPins(PressedPins,ReadKeypad.__ReasignmentIndex__)
        #pressed = []
        for pos in PressedPoses:
            if pos in ButtonAssignments:
                pressed.append(ButtonAssignments[pos])
            else:
                pressed.append(pos)
        Operation = ""
        if len(pressed) > 0:
            Operation = pressed.pop(0)
        if Operation == "Configure Graph":
            return Calculations
        if Operation == "<Del":
            Calculation = list(Calculation[0])
            Calculation.pop(cursor-1)
            cursor = cursor-1
            Calculation = "".join(Calculation)
            Calculations[Calc_Num-1][0] = Calculation
        elif Operation == "<-":
            cursor = cursor-1
        elif Operation == "->":
            cursor = cursor+1
        elif Operation == ">>":
            Calc_Num+=1
        elif Operation == "<<":
            Calc_Num-=1
        else:
            if Operation != "" and type(Operation) == type(""):
                Calculation = list(Calculation)
                Calculation.insert(cursor,Operation)
                Calculation="".join(Calculation)
                Calculations[Calc_Num-1][0] = Calculation
                cursor +=1
        if Calc_Num > Total_Calc:
            Calculations.append(["y=x",(0,0,0)])
            Total_Calc = len(Calculations)
            print(Total_Calc)
            Calc_Num = Total_Calc
        if Calc_Num <= 0:
            #Calculations.append(["y=",(0,0,0)])
            Total_Calc = len(Calculations)
            print(Total_Calc)
            Calc_Num = Total_Calc
        Calculation = Calculations[Calc_Num-1][0]
        Calc_temp = list(Calculation)
        Calc_temp.insert(cursor," ")
        Equation = label.Label(terminalio.FONT, text="".join(Calc_temp), color=0x000000)
        Equation.x = 7
        Equation.y = 55
        image[Equation_Index] = Equation
        
        CursorSymb = label.Label(font, text=(" "*(cursor-1))+"I", color=0x000000)
        CursorSymb.x = 12
        CursorSymb.y = 55
        image[Cursor_Index] = CursorSymb
        display.refresh()
        CalcIndex = label.Label(terminalio.FONT, text="{0}/{1}".format(Calc_Num,Total_Calc), color=0x000000)
        CalcIndex.x = 7
        CalcIndex.y = 14
        image[CalcIndexIndex] = CalcIndex
        display.refresh()

if __name__ == "__main__":
    displayio.release_displays()

    #spi = busio.SPI()
    tft_cs = board.GP21
    tft_dc = board.GP22

    spi = busio.SPI(board.GP26,board.GP27,board.GP28)
    display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.GP20)

    display = ST7735R(display_bus, width=160, height=128, rotation=90, bgr=True,auto_refresh=False)
    UI(display)