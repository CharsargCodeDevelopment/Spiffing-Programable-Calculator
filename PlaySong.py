from AudioOut import buzzer,ON,OFF,Set_Amplitude,note_to_frequency
import time
notes = [('e',1,0.15,1),('e',1,0.15,1),('c',1,0.15,0),('e',1,0.15,1),('c',1,0.15,0),('c',1,0.15,1),('e',1,0.3,1),('g',1,0.3,1),('c',1,0.3,0),('g',0,0.3,1)]

Octave_BOOST = 4
for note in notes:
    buzzer[0].frequency = int(note_to_frequency(note[0],note[1]+Octave_BOOST))
    buzzer[1].frequency = int(note_to_frequency(note[0],note[1]+Octave_BOOST-1))
    Set_Amplitude(note[3],0)
    Set_Amplitude(note[3],1)
    time.sleep(note[2]*0.9)
    Set_Amplitude(0,0)
    Set_Amplitude(0,1)
    time.sleep(note[2]*0.1)

#Set_Amplitude(1)
    