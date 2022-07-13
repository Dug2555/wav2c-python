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

	

file = wave.open(fileName, "rb")
output = wave.open("short.wav", "w")
hold = []

for i in range(file.getnframes()):
    chunk = file.readframes(3)
    silent = True
    for j in range(len(chunk)):
        print(chunk[j])
        if chunk[j] != 128:
            silent = False
            break
    if silent == False:
        hold.append(chunk)


output.setparams(file.getparams())
output.setnframes(len(hold))
for val in hold:
    output.writeframes(val)