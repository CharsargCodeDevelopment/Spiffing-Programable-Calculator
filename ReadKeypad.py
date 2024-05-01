import DigitalPin
import pins
import basic
import board
import time
av = 0
values = []

def ReassignPins(pins,toreasign=[],onlyconsiderX = True, KeepY = True):
    output = []
    for pin in pins:
        searchpin = pin
        if onlyconsiderX:
            searchpin = (pin[0],0)
        if searchpin in toreasign:
            if KeepY:
                outpin = (toreasign[searchpin][0],pin[1])
                output.append(outpin)
            else:
                output.append(toreasign[searchpin])
        else:
            output.append(pin)
    return output
__ReasignmentIndex__={(8,0):(0,0),(0,0):(2,0),(9,0):(3,0),(5,0):(4,0),(4,0):(5,0)}
def ReadPins():
    pins.digital_write_pin(DigitalPin.P15,True)
    time.sleep(0.01)
    pins.digital_write_pin(DigitalPin.P15,False)
    values = []
    for x in range(10):
        y = 0
        pins.digital_write_pin(DigitalPin.P16,True)
        time.sleep(0.01)
        pins.digital_write_pin(DigitalPin.P16,False)
        #values = []
        i = 0
        for pin in [board.GP11,board.GP12,board.GP13,board.GP14,board.GP15]:
            value = (pins.digital_read_pin(pin))
            if value:
                value = 1
                values.append((x,y))
            else:
                value = 0
            #print (value,end = ";")
            #for _ in range(3):
             #   av = 0.5*(av+value)
            #av = 0.01*round(av*100)
            #print()
            i+=1
            y+=1
        #print()
        #time.sleep(0.1)
    #print(values)
    #print('----------')
    return values
if __name__ == '__main__':
    while True:
        values = ReadPins()
        print(ReassignPins(values,{(8,0):(0,0),(0,0):(2,0),(9,0):(3,0),(5,0):(4,0),(4,0):(5,0)}))
