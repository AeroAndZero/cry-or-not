import json
import numpy as np

with open('data.json','r') as dataFile:
	data = (json.load(dataFile))
	mfccs = np.array(data["mfcc"])
	print(mfccs.shape)