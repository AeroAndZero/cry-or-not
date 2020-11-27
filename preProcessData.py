import librosa, librosa.display
import matplotlib.pyplot as plt
import numpy as np
import json

data = {
	"mfcc" : [],
	"label" : []
}

audioFiles = np.load("fileNames.npy")
n_fft = 2048
hop_length = 512
sr = 22050
SAMPLE_LENGTH = sr * 60

for audioData in audioFiles:
	print("Processing file : ",audioData[0])
	signal, sr = librosa.load("" + str(audioData[0]),sr=22050)

	#MFCCs
	#MFCC = librosa.feature.mfcc(signal[:SAMPLE_LENGTH], sr=sr, n_fft=n_fft, hop_length=hop_length, n_mfcc = 13)
	MFCC = librosa.feature.mfcc(signal, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mfcc = 13)
	'''
	librosa.display.specshow(MFCCs, sr=sr, hop_length=hop_length)
	plt.xlabel("Time")
	plt.ylabel("Freq")
	plt.colorbar()
	plt.show()
	'''
	MFCC = MFCC.T

	i = 0
	while (i + 100) < MFCC.shape[0]:
		smallMFCC = MFCC[i:i+100]
		i += 100
		data["mfcc"].append(smallMFCC.tolist())
		data["label"].append(audioData[1])
	print("This song had the value of i = ",i)

with open('data.json','w') as dataFile:
	json.dump(data,dataFile)