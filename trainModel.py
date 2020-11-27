import json
import numpy as np
from sklearn.model_selection import train_test_split
import keras
import matplotlib.pyplot as plt

#Plotting the graph
def plot_history(history):
    fig, axs = plt.subplots(2)
    # create accuracy sublpot
    axs[0].plot(history.history["accuracy"], label="train accuracy")
    axs[0].plot(history.history["val_accuracy"], label="test accuracy")
    axs[0].set_ylabel("Accuracy")
    axs[0].legend(loc="lower right")
    axs[0].set_title("Accuracy eval")
    # create error sublpot
    axs[1].plot(history.history["loss"], label="train error")
    axs[1].plot(history.history["val_loss"], label="test error")
    axs[1].set_ylabel("Error")
    axs[1].set_xlabel("Epoch")
    axs[1].legend(loc="upper right")
    axs[1].set_title("Error eval")
    plt.show()

data = 0
with open("data.json","r") as jsonData:
	data = json.load(jsonData)

X = np.array(data["mfcc"])
X = X[...,np.newaxis]

y = np.array(data["label"])
y = y.astype(np.int)

print(X[0][0])
print(y)

#Splitting data
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3)

#Simple MLP model
'''
model = keras.Sequential([
	keras.layers.Flatten(input_shape=(X.shape[1],X.shape[2])),

	keras.layers.Dense(512,activation='relu'),
	keras.layers.Dropout(0.3),

	keras.layers.Dense(256,activation='relu'),
	keras.layers.Dropout(0.3),

	keras.layers.Dense(64,activation='relu'),
	keras.layers.Dropout(0.3),

	keras.layers.Dense(2,activation='softmax')

	])
'''

#Convolutional Neural Network

model = keras.Sequential()

#1st layer
model.add(keras.layers.Conv2D(32,(3,3), activation='relu',input_shape=(X.shape[1],X.shape[2],1)))
model.add(keras.layers.MaxPooling2D((3,3),strides=(2,2),padding='same'))
model.add(keras.layers.BatchNormalization())
model.add(keras.layers.Dropout(0.3))

#2nd layer
model.add(keras.layers.Conv2D(32, (3, 3), activation='relu'))
model.add(keras.layers.MaxPooling2D((3, 3), strides=(2, 2), padding='same'))
model.add(keras.layers.BatchNormalization())
model.add(keras.layers.Dropout(0.3))

#3rd Layer
model.add(keras.layers.Conv2D(32, (2, 2), activation='relu'))
model.add(keras.layers.MaxPooling2D((2, 2), strides=(2, 2), padding='same'))
model.add(keras.layers.BatchNormalization())
model.add(keras.layers.Dropout(0.3))

#Flatten output
model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(64, activation='relu'))
model.add(keras.layers.Dropout(0.3))

#Output layer
model.add(keras.layers.Dense(2,activation='softmax'))

#Optimizer
optimiser = keras.optimizers.Adam(learning_rate = 0.0001)

#Compiling model
model.compile(optimizer=optimiser,
			loss='sparse_categorical_crossentropy',
			metrics=['accuracy'])

model.summary()

#Training the model
history = model.fit(X_train, y_train, validation_data=(X_test,y_test), batch_size = 32, epochs = 100)

plot_history(history)

#Saving model
model.save("sadSongClassifier")

#Model input shape : (1,100,13)