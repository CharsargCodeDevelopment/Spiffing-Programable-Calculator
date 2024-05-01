import time

from sys import stdin

import uselect

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

display = ST7735R(display_bus, width=160, height=128, rotation=90, bgr=True,auto_refresh=True)

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
x,y = 0,0
W,H = 60,60
while True:

  select_result = uselect.select([stdin], [], [], 0)

  buffer = ''

  while select_result[0]:

    input_character = stdin.read(1)

    if input_character != ',':

        buffer += input_character
        if x < W :
            x+=1
        else:
            x=0
            if y<H:
                y+=1
            else:
                y=0

    else:
        if "R" in buffer:
            x,y = 0,0
        elif "SW" in buffer:
            #print("".join(buffer.split("SW")))
            W = int("".join(buffer.split("SW")))
        elif "SH" in buffer:
            H = int("".join(buffer.split("SH")))
        else:
            r,g,b  =buffer.split(':')
            #print(r,g,b)
            #print(x,y)
            SetPixel(int(x),int(y),int(r),int(g),int(b),center=(0,0))

        print(buffer)
        
        buffer = ''

    select_result = uselect.select([stdin], [], [], 0)