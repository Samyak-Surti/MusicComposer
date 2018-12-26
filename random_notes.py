#Import the library

from midiutil.MidiFile import MIDIFile
import random

# Create the MIDIFile Object with 1 track
MyMIDI = MIDIFile(1)

# Tracks are numbered from zero. Times are measured in beats.

track = 0   
time = 0

# Add track name and tempo.
MyMIDI.addTrackName(track,time,"Sample Track")
MyMIDI.addTempo(track,time,120)

# Add a note. addNote expects the following information:
pitch_list = [60,62,64,65,67,69,71,72,71,69,67,65,64,62,60]
track = 0
channel = 0
pitch = []
time = 0
duration = 1
volume = 100
phrase_length = input("Enter length of phrase: ")

# Now add the note.
for i in range(phrase_length):
	pitch.append(random.randint(60,72))
	print pitch
	for j in pitch:
		MyMIDI.addNote(track,channel,j,time,duration,volume)
		time += 1



# And write it to disk.
binfile = open("output.mid", 'wb')
MyMIDI.writeFile(binfile)
binfile.close()
