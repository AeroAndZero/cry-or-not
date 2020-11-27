import json
import numpy as np
import keras
import librosa

n_fft = 2048
hop_length = 512
sr = 22050
SAMPLE_LENGTH = sr * 60

model = keras.models.load_model('sadSongClassifier')

'''
data = 0
with open("data.json","r") as jsonData:
	data = json.load(jsonData)
'''
def main(filePath):
	signal, sr = librosa.load(filePath,sr=22050)
	MFCC = librosa.feature.mfcc(signal, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mfcc = 13)
	MFCC = MFCC.T

	i = 0
	totalY = 0
	sumOfY = 0
	while (i + 100) < MFCC.shape[0]:
		smallMFCC = MFCC[i:i+100]
		i += 100

		X_new = np.array(smallMFCC)
		X_new = X_new[np.newaxis ,..., np.newaxis]
		print(X_new.shape)

		y_predict = model.predict_classes(X_new)

		totalY += 1
		sumOfY += y_predict[0]

		print("Predicted : {}, Total average : {}".format(y_predict,sumOfY/totalY))

	print("Final result : ",(sumOfY/totalY*100),"%")
	return sumOfY/totalY

if __name__ == '__main__':
	main("42.m4a")