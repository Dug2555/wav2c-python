import soundfile as sf
import wave
import numpy as np
import sys
import librosa

if len(sys.argv) < 3:
	exit()
else:
	fileName = str(sys.argv[1])
	hfile = str(sys.argv[2])


d, s = librosa.load(fileName, sr=8000)
print("lib")
sf.write(fileName, d, s, subtype= 'PCM_U8')

wav = wave.open(fileName)
if wav.getnchannels() >= 2:
	channels = wav.getnchannels()
	sdata = wav.readframes(wav.getnframes())
	params = wav.getparams()
	data = np.fromstring(sdata, dtype=np.uint8)
	ch_data = data[0::channels]
	wav.close()
	outwav = wave.open("ShortEdit.wav", "w")
	outwav.setparams(params)
	outwav.setnchannels(1)
	outwav.writeframes(ch_data.tostring())
	outwav.close()
else:
	wav.close()

	

file = open(fileName, "rb")
hold = []

while True:
	chunk = file.read(44)
	if chunk == b"":
		break
	hold.append(chunk)
file.close()

file.close()
size = (len(hold) - 1) * 44
print()
print(hold[0])

output = open(hfile, "w")
holderString = ""
clean = 0
for i in hold:
	if i == 0:
		continue
	for j in i:
		holderString += hex(j)
		if hex(j) == '0x80':
			clean += 1
		elif clean > 0:
			clean = 0
		holderString += ", "
		if clean >= 5:
			holderString = holderString[:-35]
			clean = 0

holderString = holderString[:-3]
holdList = holderString.split(", ")
print(len(holdList))
for val in holdList:
	if len(val) != 4:
		print(val)
		holdList.remove(val)

output.write("const unsigned char song [" + str(len(holdList)) + "] = {")
output.write(", ".join(holdList))
output.write("\n};")