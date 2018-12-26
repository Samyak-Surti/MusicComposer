############################################################################
# A sample program to create a single-track MIDI file, add a note,
# and write to disk.
############################################################################

#Import the library
from midiutil.MidiFile import MIDIFile

# Create the MIDIFile Object
MyMIDI = MIDIFile(1)

# Add track name and tempo. The first argument to addTrackName and
# addTempo is the time to write the event.
track = 0
time = 0
MyMIDI.addTrackName(track,time,"Sample Track")
MyMIDI.addTempo(track,time, 120)

# Add a note. addNote expects the following information:
channel = 0
pitch = 60
duration = 1
volume = 100
note_list = [60,61,62,63,64,65,66,67,68,69,70]
for i in note_list:
	MyMIDI.addNote(track,channel,i,time,duration,volume)

# Now add the note.
#MyMIDI.addNote(track,channel,pitch,time,duration,volume)

# And write it to disk.
binfile = open("output.mid", 'wb')
MyMIDI.writeFile(binfile)
binfile.close()

