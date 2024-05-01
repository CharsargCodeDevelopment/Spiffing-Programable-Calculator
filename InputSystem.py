import digitalio
import board
import analogio
from board import *
import time
pin = digitalio.DigitalInOut(board.LED)

InputPins = [board.GP4,board.GP6,board.GP7,board.GP8]
OutputPins = [board.GP15,board.GP14,board.GP13,board.GP12,board.GP11,board.GP9]
ResetPin = board.GP0
ClockPin=board.GP1

ResetPin = digitalio.DigitalInOut(ResetPin)
ClockPin = digitalio.DigitalInOut(ClockPin)
ResetPin.direction = digitalio.Direction.OUTPUT
ClockPin.direction = digitalio.Direction.OUTPUT

for i in range(len(InputPins)):
    InputPins[i] = digitalio.DigitalInOut(InputPins[i])
for i in range(len(OutputPins)):
    #OutputPins[i] = analogio.AnalogIn(OutputPins[i])
    OutputPins[i] = digitalio.DigitalInOut(OutputPins[i])
def SCAN_PINS():
    Pressed = []
    #ResetPin.value = True
    #time.sleep(0.5)
    #ResetPin.value = False
    for Y in range(6):
        #Row = InputPins[Y]
        #Row.direction = digitalio.Direction.OUTPUT
        #Row.value = True
        for X in range(len(OutputPins)):
            Col = OutputPins[X]
            #print(Col.value)
            if Col.value:
                Pressed.append((X,Y))
                print(1,end="")
            else:
                print(0,end="")
        #Row.value = False
        time.sleep(0.5)
        ClockPin.value = True
        time.sleep(0.4)
        ClockPin.value = False
        print()
    print(Pressed)
    #ClockPin.value = True
    #time.sleep(0.1)
    #ClockPin.value = False
    """
    for _ in range(10-len(InputPins)):
        ClockPin.value = True
        time.sleep(0.1)
        ClockPin.value = False
        time.sleep(0.1)
    """
    #time.sleep(0.05)
    print('-'*len(OutputPins))
    return Pressed

if __name__ == '__main__':
    import time
    while True:
        SCAN_PINS()
        time.sleep(0.1)

