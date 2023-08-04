from fileinput import filename
import librosa
import soundfile as sf
import wave
import numpy as np
import sys

#Gets User Input
if len(sys.argv) < 3:
	exit()
else:
	fileName = str(sys.argv[1])
	hfile = str(sys.argv[2])

#Loads the file into librosa to change the WAV format to PCM_U8
d, sr = librosa.load(fileName, sr=8000)
sf.write(fileName, d, sr, subtype= 'PCM_U8')

#This section is to make sure that the WAV file is only one channel
wav = wave.open(fileName)
if wav.getnchannels() >= 2:
	channels = wav.getnchannels()
	sdata = wav.readframes(wav.getnframes())
	params = wav.getparams()
	wav.close()

	#Turns the gathered data from a string into useable data
	data = np.fromstring(sdata, dtype=np.uint8)
	ch_data = data[0::channels]
	
	#This recreates the file as a one channel WAV with all the same data that was on the original file
	outwav = wave.open(fileName, "w")
	outwav.setparams(params)
	outwav.setnchannels(1)
	outwav.writeframes(ch_data.tostring())
	outwav.close()
else:
	wav.close()

	
#Opens the files as bytes to read
file = open(fileName, "rb")

#Creates an array with each chunk of 44 bytes
hold = []
while True:
	chunk = file.read(44)
	if chunk == b"":
		break
	hold.append(chunk)
file.close()

#Sets the size for use in a conditional
size = (len(hold) - 1) * 44

#Writes the data gathered into a .h file with proper formatting
output = open(hfile, "w")
output.write("const unsigned char song [" + str(size) + "] = {")
byteOutput = ""
for i in hold:
	if i == 0:
		continue
	for j in i:
		byteOutput += hex(j)
		byteOutput += ", "
	byteOutput += "\n"

#Removes the newline and comma that was added on the end
output.write(byteOutput[:-3])

output.write("\n};")