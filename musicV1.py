from midiutil.MidiFile import MIDIFile
import random
import datetime
import os

Debug = False


# This function creates a file for each matrix created so that they are saved.
def rw_melody_file(file):
	file_list = []
	true_file_list = []
	with open(file,'rw') as file_handle:
		note_file = file_handle.read().splitlines()
		for i in note_file:
			file_list.append(i)
		for j in file_list:
			file_list = j.split()
			for k in file_list:
				true_file_list.append(k)
		return true_file_list	
	file_handle.close()
	
def write_melody_file(melody):
	melody_name = (datetime.datetime.now().strftime("%Y-%m-%d%H:%M:%S") + '.txt')
	file_handle = open(melody_name,'w')
	file_handle.write(str(melody))
	return file_handle
	


# This function reads a text file and increments matrices accordingly.
def train_matrix(list,input_matrix,pitch_dict):
	note1 = ''
	note2 = ''
	#print list
	for i in range(len(list) - 1):
		note1 = define_note_value(list[i],pitch_dict)
		note2 = define_note_value(list[i+1],pitch_dict)
		if Debug == True:
			print i
			print note1
			print "This is note 1"
			print note2
			print "This is note 2"
		input_matrix[note1][note2] += 1
	return input_matrix
	
# Also trains matrix but assumes that note_values are already accessible.
def train_matrix2(notes,in_matrix):
	note1 = ''
	note2 = ''
	#print len(notes)
	for i in range(len(notes) - 1):
		note1 = notes[i]
		note2 = notes[i+1]
		in_matrix[mod12_note_value(note1)][mod12_note_value(note2)] += 1
	return in_matrix

# This function creates matrix file every time matrix is trained.
def write_matrix_file(matrix):
	matrix_File = open('matrix_File.txt','w')
	matrix_File.write(str(matrix))
	matrix_File.close()

# Reads existing matrix file so that it can be used	
def read_matrix_file(matrix_file):
	file_handle = open(matrix_file,'r')
	return eval((file_handle.read()))

	
# Converts pitch value of note into a proper MIDI value.
def convert_to_midi(note,pitch_dict):
	octave = 5
	note = str(note)
	midi_number = 12*(octave) + int(define_note_value(note,pitch_dict))
	return midi_number
	
# This will give a proper pitch value between zero and eleven if above function does not produce value in that range.		
def mod12_note_value(note_val):
	mod12_val = note_val % 12
	return mod12_val
	
# Converts already determined pitch value of note into a proper MIDI value.
def convert_to_midi2(note_val):
	octave = 5
	#octave_shift_val = 0
	#if (note_val/12) > 1:
	#	octave_shift_val = note_val/12
	#	octave += octave_shift_val
	#if (note_val/12) < 0:
	#	octave_shift_val = note_val/12
	#	octave = octave - octave_shift_val
	midi_number = 12*(octave) + (int(note_val))
	#print midi_number
	return midi_number

# This function makes it easy to distinguish between enharmonic notes.
def define_note_value(note,pitch_dict):
	note_value = 0
	#print note[0]
	if note[1:] == '#':
		note_value = int(pitch_dict[note[0]]) + 1
	elif note[1:] == 'b':
		note_value = int(pitch_dict[note[0]]) - 1
	elif note[1:] == "'":
		note_value = int(pitch_dict[note[0]]) + 12
	else:
		note_value = int(pitch_dict[note[0]])
	return mod12_note_value(note_value)
	
	
# Will make matrix easy to read
def print_matrix(matrix,num_rows,num_columns):
	num_row = 0	
	for i in range(num_rows):
		row = ''
		for j in range(num_columns):
			row += str(matrix[i][j]) + ' '
		print (row)
			
# This function will find a random i value of the matrix that will serve as a starting note.
def find_start_note(trained_matrix,num_rows):
	valid_note = False
	while valid_note == False:
		starting_note = random.randrange(num_rows)
		for i in range(num_rows):
			if trained_matrix[starting_note][i] != 0:
				valid_note = True
				break
	return starting_note

# If we have it such that one note leads back to the same note, Markov Chain will make it such that it will be stuck in the same loop forever.
def remove_self_loop(trained_matrix,num_rows):
	for i in range(num_rows):
		trained_matrix[i][i] = 0

# This function will figure out, based on the weights of the matrix, which notes to play.		
def make_phrase(trained_matrix,starting_note,num_columns,num_rows,phrase_length):
	phrase = []
	phrase.append(starting_note)
	possible_note_options = []
	max_weight = ''
	next_note_list = []
	append_list = ''
	current_phrase_length = 1
	while current_phrase_length < phrase_length:
		for i in range(num_columns):
			possible_note_options.append(trained_matrix[int(starting_note)][i])
		if Debug == True:
			print possible_note_options
			print "This is all possible note options"
		for j in range(len(possible_note_options)):
			if possible_note_options[j] != 0:
				append_list = str(str(possible_note_options[j]) * j)
				for k in append_list:
					next_note_list.append(str(k))
					
		if Debug == True:
			print "This is next note list"
			print next_note_list	
		if next_note_list == []:
			next_note = find_start_note(trained_matrix,num_rows)
		else:
			next_note = random.choice(next_note_list)
		phrase.append(int(next_note))
		starting_note = next_note
		current_phrase_length += 1
		possible_note_options = []
		next_note_list = []
		append_list = ''
	if Debug == True:
		print phrase
		print "This is start_phrase"
	return phrase
	
	
# Translates by shifting certain number of semi-tones up or down.
def shift_phrase(phrase,shift_value):
	for i in range(len(phrase)):
		phrase[i] += shift_value
	if Debug == True:
		print 'IN SHIFT FUNC'
		print len(phrase)
		print " This is length of phrase"
	return phrase

# Reverses order of notes in initial phrase
def reverse_phrase(phrase):
	reversed_phrase = []
	phrase.reverse()
	reversed_phrase = phrase
	if Debug == True:
		print 'IN REVERSE FUNC'
		print reversed_phrase
		print "This is the reversed phrase"
	return reversed_phrase
	
def rotate_phrase(phrase,rotate_mag):
	modn = rotate_mag % len(phrase)
	if Debug == True:
		print 'IN ROTATE FUNC'
	return (phrase[modn:] + phrase[0:modn])

	
def choose_transformation(phrase):
	transform_choice = random.choice(transformation_choices)
	rotate_magnitude = random.randint(0,len(phrase))
	if transform_choice == 'shift':
		shift_value = random.randrange(-12,13)
		if Debug == True:
			print 'shift'
			print phrase
			print "This is the original phrase"
			print (shift_phrase(phrase,shift_value))
			print "This is the shifted phrase"
		return (shift_phrase(phrase,shift_value))
	elif transform_choice == 'reverse':
		if Debug == True:
			print 'reverse'
		return (reverse_phrase(phrase))
	else:
		if Debug == True:
			print 'rotate'
		return (rotate_phrase(phrase,rotate_magnitude))
		
		
# Takes in different durations of notes
#def add_rhythm_overlay(note,duration):
	
# This will combine all of the different phrases together.
def make_music(phrase_set_length,trained_matrix,starting_note,num_columns,num_rows,phrase_length):
	phrase_count = 0
	music_notes = []
	start_phrase = []
	random_loop_count = 0
	transform_phrase = []
	while phrase_count < phrase_set_length:
		start_phrase = (make_phrase(trained_matrix,starting_note,num_columns,num_rows,phrase_length))
		if Debug == True:
			print start_phrase
			print "This is start phrase"
		music_notes += start_phrase
		phrase_count += 1
		random_loop_count = random.randint(0,(phrase_set_length - phrase_count))
		for i in range(random_loop_count):
			transform_phrase = (choose_transformation(start_phrase))
			music_notes += transform_phrase
			phrase_count += 1
	return music_notes

def user_opinion(user_in,melody,input_matrix,starting_note,num_columns,num_rows,phrase_length,phrase_set_length,pitch_dict):
	trained_matrix = []
	start_phrase = []
	new_melody = []
	if user_in == 'Y':
		melody_handle = write_melody_file(melody)
		print "The melody you liked has now been saved as a seperate file."
		print "This new file will now be used to train another empty matrix to produce more music to your taste."
		trained_matrix = train_matrix2(melody,input_matrix)
		start_phrase = make_phrase(trained_matrix,starting_note,num_columns,num_rows,phrase_length)
		new_melody = make_music(phrase_set_length,trained_matrix,starting_note,num_columns,num_rows,phrase_length)
		if Debug == True:
			print new_melody
			print "This is the new melody"
		return new_melody
	else:
		new_pref = input("Would you like to train the matrix with another melody('Y','N')?: ")
		if new_pref == 'Y':
			new_pref_choice = input("Enter the name of the new melody you would like to use to train: ")
			trained_matrix = train_matrix(rw_melody_file(new_pref_choice),input_matrix,pitch_dict)
			start_phrase = make_phrase(trained_matrix,starting_note,num_columns,num_rows,phrase_length)
			new_melody = make_music(phrase_set_length,trained_matrix,starting_note,num_columns,num_rows,phrase_length)
			return new_melody
		else:
			#print "Thank you for your time! "
			return None 
		

# This function will be made to use a trained matrix
#def matrix_trained_use():
	
# This function reads a scale file if a certain key has been requested by the user
#def read_scale(scale_file):

# east_mid = {'S':60,'r':61,'R':62,'g':63,'G':64,'m':65,'M':66,'P':67,'d':68,'D':69,'n':71,'N':72}
notes_dict = {'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}

				
# Will make so that it will recognize notes such as C# and Db as having the same value.
#def enharmonic_notes():

trained_matrix = [[]]
trained_matrix = [[0 for i in range(12)] for j in range(12)]
empty_matrix = [[0 for k in range(12)] for l in range(12)]
num_rows = 12
num_columns = 12 

#trained_matrix = train_matrix(rw_melody_file('pilu.txt'),matrix,notes_dict)
#print_matrix(trained_matrix,num_rows,num_columns)
#print rw_melody_file('pilu.txt')
#note = 'Cb'
#value = (define_note_value(note,notes_dict))
#print value

starting_note2 = ''
user_response = 'Y'
existing_matrix = []
new_phrase = []
new_melody = []
user_in2 = input("Do you want to choose (a) file(s) to train an empty matrix,or would you like to choose an existing trained matrix('0','1')?: ")
if user_in2 == '0':
	while user_response == 'Y':
		file_Name_in = input("Enter the name of the file you wish to use: ")
		saved_files_List = []
		saved_files_List.append(file_Name_in)
		user_response = input("Would you like to enter another file? (Y or N): ")
		trained_matrix = train_matrix(rw_melody_file(file_Name_in),trained_matrix,notes_dict)
		write_matrix_file(trained_matrix)
		print "The file you entered has now been saved."
		if user_response == 'N':
			break
elif user_in2 == '1':
	trained_matrix = read_matrix_file('matrix_File.txt')

	
		
		

remove_self_loop(trained_matrix,num_rows)
		
			

MyMIDI = MIDIFile(1)
MyMIDI2 = MIDIFile(1)


#MyMIDI.addTrackName(track,time,"Sample Track")
#MyMIDI.addTempo(track,time,120)

track = 0
channel = 0
#pitch = []
time = 0
duration = 1
volume = 100
shift_value = 0
transformation_choices = ['shift','reverse','rotate']
# Choices to add: 'rotate','invert'
notes_to_play = []
#time_of_day = ''
#time_of_day = str(time.strftime("%I:%M:%S"))
#print time_of_day


MyMIDI.addTempo(track,time,200)
MyMIDI2.addTempo(track,time,200)


notes_Play_list = []
music_length = 0
phrase_length = input("Enter how long you would like to have the phrase be: ")
phrase_set_length = input("Enter the number of phrases you would like to have created: ")
starting_note = find_start_note(trained_matrix,num_rows)
notes_Play_list = make_music(phrase_set_length,trained_matrix,starting_note,num_columns,num_rows,phrase_length)
music_length = len(notes_Play_list)
note_vol = 100


print notes_Play_list
for d in range(music_length - 1):
	if int(notes_Play_list[d]) > int(notes_Play_list[d-1]) or int(notes_Play_list[d]) > int(notes_Play_list[d + 1]):
		note_vol = 120
		MyMIDI.addNote(track,channel,convert_to_midi2(notes_Play_list[d]),time,duration,note_vol)
		time += 1
	else:
		note_vol = 80
		MyMIDI.addNote(track,channel,convert_to_midi2(notes_Play_list[d]),time,duration,note_vol)
		time += 1
print "Listen to example."

binfile = open("output.mid", 'wb')
MyMIDI.writeFile(binfile)
binfile.close()


user_input = input("Did you like the example that was generated('Y','N')?: ")
notes_Play_list = user_opinion(user_input,notes_Play_list,empty_matrix,starting_note,num_columns,num_rows,phrase_length,phrase_set_length,notes_dict)
if notes_Play_list != None:
	music_length = len(notes_Play_list)
	for j in range(music_length - 1):
		if int(notes_Play_list[j]) > int(notes_Play_list[j-1]) or int(notes_Play_list[j]) > int(notes_Play_list[j + 1]):
			note_val = 120
			MyMIDI2.addNote(track,channel,convert_to_midi2(notes_Play_list[j]),time,duration,note_val)
			time += 1
		else:
			note_val = 80
			MyMIDI2.addNote(track,channel,convert_to_midi2(notes_Play_list[j]),time,duration,note_val)
			time += 1
	print "Listen to second example"
else:
	print "Thank you for your time"

		


binfile2 = open("output2.mid", 'wb')
MyMIDI2.writeFile(binfile2)
binfile2.close()
