import tkinter as tk
from tkinter import filedialog
import os
import moviepy.editor as mp
import testModel
import threading
import time

def browseFileFunc(vpEntry):
    #Reading The File
    vpEntry.delete(0,tk.END)
    ftype = [('MPEG-4','*.mp4')]
    dlg = filedialog.Open(filetypes = ftype)
    fp = dlg.show()	#Gives path of the open file
    fp = fp.replace("/","\\")
    vpEntry.insert(0,fp)

def openFileFunc(vpEntry):
	fp = vpEntry.get()
	os.system("\""+fp+"\"")

def extractAudio():
	fp = vpEntry.get()
	clip = mp.VideoFileClip(fp)
	clip.audio.write_audiofile("./temp.wav",codec='pcm_s16le')

def analyseFunc(titleLabel):
	global status,root

	status.set("Extracting Audio...")
	root.update()
	extractAudio()

	status.set("Analysing...")
	root.update()

	result = testModel.main("./temp.wav")
	resultRounded = round(result*100,2)
	if(resultRounded > 50):
		status.set("Answer : Yes, Prediction : "+ str(resultRounded) +" %")
	else:
		status.set("Answer : No, Prediction : "+ str(resultRounded) +" %")
	root.update()

#Config window
root = tk.Tk()
root.title("Cry or not")
root.geometry("600x150")

#Defining GUI -> 3x4 grid
root.columnconfigure(0,weight=1)
root.columnconfigure(1,weight=4)
root.columnconfigure(2,weight=4)
root.columnconfigure(3,weight=1)

root.rowconfigure(0,weight=1)
root.rowconfigure(1,weight=1)
root.rowconfigure(2,weight=1)

#Title label
status = tk.StringVar()
status.set("Will The Judges Cry ?")
wtjc = tk.Label(root,textvariable=status,font=("Arial", 22))
wtjc.grid(row=0,column=0,columnspan=4)

#Video path label
vpLabel = tk.Label(root,text="Video path : ")
vpLabel.grid(row=1,column=0)

#Video path entry
vpEntry = tk.Entry(root)
vpEntry.grid(row=1,column=1,columnspan=2,padx=5,pady=20,sticky="news")

#Browse button
browse = tk.Button(root,text="Browse",command = lambda : browseFileFunc(vpEntry))
browse.grid(row=1,column=3,padx=5,pady=5,sticky="news")

#Analyse button
analyse = tk.Button(root,text="Analyse",command = lambda: analyseFunc(wtjc))
analyse.grid(row=2,column=0,columnspan=2,padx=25,pady=5,sticky="news")

#Open button
openFile = tk.Button(root,text="Open File", command = lambda : openFileFunc(vpEntry))
openFile.grid(row=2,column=2,columnspan=2,padx=25,pady=5,sticky="news")

root.mainloop()
