from os import walk
import os
import sys
import numpy as np
import json
import pafy

fileNames = []

def download(link,fileNumber):
	result = pafy.new(link)
	best_quality_audio = result.getbestaudio(preftype = "m4a")
	print(best_quality_audio)
	best_quality_audio.download(filepath=str(fileNumber)+".m4a")
	#return (result.title)
	return str(fileNumber)

#download("https://www.youtube.com/watch?v=jFGKJBPFdUA",42)

''''''
with open("videoLinks.json") as jsonData:
	audiolist = json.load(jsonData)

	i = 1
	for link in audiolist["videoLink"]:
		fileNames.append([download(link[0],i) + ".m4a",link[1]])
		i+=1

fileNames = np.array(fileNames)
print(fileNames)
np.save("fileNames.npy",fileNames)
