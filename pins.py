import digitalio
import board
import analogio  # Import the analogio module
pin = digitalio.DigitalInOut(board.LED)
print(pin.value)



def digital_read_pin(pinValue):
    try:
        pin = digitalio.DigitalInOut(pinValue)
        __pins__[pinValue] = pin
    except ValueError:
        pin = __pins__[pinValue]
    #pin = digitalio.DigitalInOut(pin)
    return (pin.value)

__pins__ = {}
def digital_write_pin(pinValue, value):
    try:
        pin = digitalio.DigitalInOut(pinValue)
        __pins__[pinValue] = pin
    except ValueError:
        pin = __pins__[pinValue]
    except:
        return
    pin.direction = digitalio.Direction.OUTPUT
    pin.value = value
    
def analog_read_pin(pin_value):
    try:
        pin = analogio.AnalogIn(pin_value)  # Initialize the AnalogIn object
        __pins__[pin_value] = pin
    except ValueError:
        pin = __pins__[pin_value]
    return pin.value