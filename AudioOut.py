import board
import pwmio
from time import monotonic,sleep
import random


pin1 = pwmio.PWMOut(board.GP15, variable_frequency=True)
pin2 = pwmio.PWMOut(board.GP12, variable_frequency=True)
pin3 = pwmio.PWMOut(board.GP11, variable_frequency=True)
pin4 = pwmio.PWMOut(board.GP9, variable_frequency=True)
pin4 = pwmio.PWMOut(board.GP7, variable_frequency=True)
buzzer = [pin1,pin2,pin3,pin4]

#buzzer.frequency = 440

OFF = 0
ON = 2**15
#buzzer.duty_cycle = ON
def Set_Amplitude(value,pin=0):
    buzzer[pin].duty_cycle = value*ON
    
def SquareSoundGenerator(Start_Htz = 440,End_Htz = 220,time = 1,pin = 0):
    start = monotonic()
    progress_time = monotonic()-start
    Delta_Htz = End_Htz-Start_Htz
    htz = Start_Htz
    buzzer.duty_cycle = ON
    while progress_time <= time:
        progress_time = monotonic()-start
        progress = progress_time/time
        htz = (Delta_Htz*progress) + Start_Htz
        buzzer[pin].frequency = int(htz)
    buzzer.duty_cycle = OFF
    print(progress_time)
    
def NoiseSoundGenerator(Start_Htz = 440,End_Htz = 220,time = 1,pin = 0):
    start = monotonic()
    progress_time = monotonic()-start
    Delta_Htz = End_Htz-Start_Htz
    htz = Start_Htz
    buzzer.duty_cycle = ON
    while progress_time <= time:
        progress_time = monotonic()-start
        progress = progress_time/time
        htz = ((Delta_Htz*progress) + Start_Htz)+random.randint(-100,100)
        buzzer[pin].frequency = int(htz)
    buzzer[pin].duty_cycle = OFF
    print(progress_time)
    

def note_to_frequency(note, octave):
    # Dictionary to map note letters to MIDI note numbers
    note_mapping = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
                    'E': 4, 'Fb': 4, 'E#': 5, 'F': 5, 'F#': 6, 'Gb': 6,
                    'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10,
                    'B': 11, 'Cb': 11, 'B#': 0}

    # Convert note letter to uppercase
    note = note.upper()

    # Calculate MIDI note number
    midi_note = note_mapping[note] + (octave + 1) * 12

    # Calculate frequency
    frequency = 440.0 * (2 ** ((midi_note - 69) / 12.0))

    return frequency


"""
NoiseSoundGenerator()
values = 100
multiplier = 1/values
Start_Htz = 440
End_Htz = 220
Delta_Htz = End_Htz-Start_Htz
for progress_time in range(values):
    progress = progress_time*multiplier
    htz1 = ((Delta_Htz*progress) + Start_Htz)+random.randint(-10,10)
    htz2 = ((Delta_Htz*progress) + Start_Htz)
    print(int(htz1),int(htz2))
"""
"""
buzzer[0].frequency = 16.35
buzzer[1].frequency = 20.60
buzzer[1].frequency = 24.50
"""
"""
octave = 4

buzzer[0].frequency = int(note_to_frequency('c',octave))
buzzer[1].frequency = int(note_to_frequency('e',octave))
buzzer[2].frequency = int(note_to_frequency('g',octave))
buzzer[2].frequency = int(note_to_frequency('c',octave+1))
buzzer[2].frequency = int(note_to_frequency('e',octave+1))

for item in buzzer:
    item.duty_cycle = ON
    sleep(1)
"""
