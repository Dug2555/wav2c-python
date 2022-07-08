from fileinput import filename
import librosa
import soundfile as sf
import wave
import numpy as np
import sys

if len(sys.argv) < 3:
	exit()
else:
	fileName = str(sys.argv[1])
	hfile = str(sys.argv[2])


d, s = librosa.load(fileName, sr=8000)
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
	chunk = file.read(40)
	if chunk == b"":
		break
	hold.append(chunk)
file.close()

file.close()
print(hold[0])

output = open(hfile, "w")
for i in hold:
	for j in i:
		output.write(hex(j))
		output.write("\n")
