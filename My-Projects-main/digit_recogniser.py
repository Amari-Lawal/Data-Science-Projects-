# -*- coding: utf-8 -*-
"""Digit Recogniser


Automatically generated by Colaboratory.



Original file is located at
    https://colab.research.google.com/drive/1Yj3PApDCOtziwvIyxETLHEVrugmefF5N

Sunday 12th December 2020
"""
#This is the Learning process and practice in order to self teach myself Deep Learning Techniques.

# I wanted to keep all the messy stuff to show my brain process in learning these techniques
# First attempt at Deep Learning and Using CNN Model with Sequential API
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn			
import sklearn.datasets	
import sklearn.linear_model		 
import sklearn.metrics
import random
import tensorflow as tf
from sklearn import tree
import random                                   #Loading Dependencies
import seaborn as sns
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import Sequential
from tensorflow.keras.layers import * 
from sklearn.metrics import confusion_matrix
import pickle
from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import train_test_split
import cv2 as cv


#Split the dimensions from (x,y) to (x,y,z)

#https://www.kaggle.com/marinescuana/digit-recognizer-tensorflow-keras
#Helped me to understand

# When createing a Neural Network model
# Firts you need to obviously shape data etc.
# Then you have to convert the needed input values into a tensor format, which is similiar to the structure of pandas and numpys.
# Set it as the dtype as tf.float32

DATA_URL = "/content/drive/MyDrive/Data Science Practice/Digit Recogniser/digit-recognizer.zip (Unzipped Files)/train.csv"
df_train = pd.read_csv(DATA_URL)
display(df_train)           # Loading in training dataset, as each pixel.

DATA_URL_TE= "/content/drive/MyDrive/Data Science Practice/Digit Recogniser/digit-recognizer.zip (Unzipped Files)/test.csv"
df_test = pd.read_csv(DATA_URL_TE)
display(df_test)      # Loading in test dataset

"""
def train_test_split(dataset):
  return np.split(dataset, [int(dataset.shape[0] * 0.5)])

labels_train, labels_test = train_test_split(labels_train)
X_train, y_test = train_test_split(X)
"""



#X = df_train.drop("label", axis = 1).values.reshape(-1, 28, 28, 1)
#labels_train = df_train["label"].values                             
#labels_test = df_train["label"].values               # Dropping the label values  from train set then reshaping it in a shape involving (num of images,height,width,channels)

#def train_test_label_split(dataset):
#  return np.split(dataset, [int(dataset.shape[0] * 0.666666667)]) # Creating my own data split function ended up using library 
  
#labels_test, Nan = train_test_label_split(labels_test) # This meant data was lost, which hopefully should be avoided.
#X_train = X

#labels_test = labels_test.reshape(28000,1)
#labels_train = labels_train.reshape(42000,1)   # Trying to individually reshape each train and test dataset
#y_test = df_test.values.reshape(-1, 28, 28, 1)
#y = y.reshape(-1,28,28,1)
#print(X_train.shape,labels_train.shape,labels_test.shape,y_test.shape) # Trying to make all dimensions equal to be used in Model

#labels_test, Nan = train_test_label_split(labels_test) 
#X_train = X

X_train = df_train.drop("label", axis = 1).values.reshape(-1, 28, 28, 1) # Drops Labels from training set and reshapes
X_test = df_test.values.reshape(-1, 28, 28, 1) # Reshapes test
y_train = df_train["label"] # Sets y as labels
X_train, X_test, y_train, y_test = train_test_split(X_train,y_train,test_size=0.1,random_state=2) # Splits into test and train

"""
inputs = Input(shape=(784,))                 # input layer
x = Dense(32, activation='relu')(inputs)     # hidden layer
outputs = Dense(10, activation='softmax')(x) # output layer       # Learning how Nerual Networks and trying to map it out simplistically

model = Model(inputs, outputs)
"""

def normalise(data):
  return data / 255     # Normalise Data
X_train = normalise(X_train)
X_test = normalise(X_test)

for i in range(1,100,1):
    plt.subplot(10,10,i);           # Visualise first 100 images
    b = plt.imshow(X_train[i-1][:,:,0],cmap=plt.get_cmap('gray'))

g = plt.imshow(X_train[4][:,:,0])

h = plt.imshow(X_train[5][:,:,0])

#Try not to use until I learn about Sessions
#X_train = tf.convert_to_tensor(X_train,dtype=tf.float32)
#y_test = tf.convert_to_tensor(y_test,dtype=tf.float32)

model = Sequential()
model.add(Conv2D(32,kernel_size=(3,3),activation='relu',input_shape=(28,28,1))); # Creates a 2d Convolution layer with batch size of 32 and kernel size filters, with rectified linear activation function
model.add(Conv2D(64,(3, 3),activation='selu')); # using activation function selu 

model.add(MaxPooling2D((2, 2))); # Using a pooling layer

model.add(Dropout(0.25)); # Dropout to make the model forget some of the data to stop overfitting

model.add(Flatten()); # Flatten to put data into one vector 


model.add(Dense(128,activation='relu')); # Apply Dense layer

model.add(Dropout(0.5)); # Dropout again to stop 

model.add(Dense(10,activation='softmax')); # Then output as the 10 outputs I want and turn them into probabilities

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), # Compile model
              metrics=['accuracy'])

history = model.fit(X_train,y_train,epochs=10,batch_size=200,validation_data=(X_test,y_test)) # Run model with 10 epoches and 200 batch size with a validation accuracy

model.summary()

score=model.evaluate(X_test,y_test,verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1]*100) # Evaluates model

yhat_test = model.predict(X_test)# Makes prediction

yhat_test.shape

def yhat_test_labels(data,index):
  arg_yhat = np.argmax(data[index])
  print("Predicted value:",arg_yhat)
def X_test_labels(data,index):
  h = plt.imshow(data[index][:,:,0])
# Trying to visualise predicted number and corresponding feature

ans = int(input("What index number do u want?"))
yhat_test_labels(yhat_test,ans)
print("Real value:")
X_test_labels(X_test,ans)
# Does it by index of the dataframe not fully refined

history_df=pd.DataFrame(history.history)
history_df.loc[:,['loss','val_loss']].plot()
history_df.loc[:,['accuracy','val_accuracy']].plot() # Plot of models performance

"""# Mushroom Recogniser"""

# Didn't finish data analysis
DATA_MUSH = "/content/drive/MyDrive/Data Science Practice/mushrooms[1].csv"
mush_df_ = pd.read_csv(DATA_MUSH)
display(mush_df)



print("Poisonous and edible:",pd.unique(mush_df.iloc[:,0]))
print("habitat: grasses=g,leaves=l,meadows=m,paths=p,urban=u,waste=w,woods=d",pd.unique(mush_df.loc[:,"habitat"]))
print("population: abundant=a,clustered=c,numerous=n,scattered=s,several=v,solitary=y",pd.unique(mush_df.loc[:,"population"]))
print("odor:almond=a,anise=l,creosote=c,fishy=y,foul=f,musty=m,none=n,pungent=p,spicy=s",pd.unique(mush_df.loc[:,"odor"]))

poison = mush_df["class"] == "p"
cols = ["class","cap-shape","cap-surface","cap-color","bruises","odor"	,"gill-attachment",	"gill-spacing",	"gill-size",	"gill-color"	,"stalk-shape"	,"stalk-root",	"stalk-surface-above-ring",	"stalk-surface-below-ring",	"stalk-color-above-ring",	"stalk-color-below-ring","veil-type",	"veil-color"	,"ring-number",	"ring-type",	"spore-print-color",	"population","habitat"]
poison_df = mush_df.loc[poison,cols]
display(poison_df)

def boolean_series(data,**color,**column,**values):
  print(("Poisonous",color,":",data.loc[:,str(column)]== str(values)).sum())




boolean_series(poison_df,brown,cap-color,"n")


"""
print(pd.unique(poison_df["cap-color"]))
print("Poisonous_brown:",(poison_df.loc[:,"cap-color"] == "n").sum())
print("Poisonous_yellow:",(poison_df.loc[:,"cap-color"] == "y").sum())
print("Poisonous_white:",(poison_df.loc[:,"cap-color"] == "w").sum())
print("Poisonous_cinnamon:",(poison_df.loc[:,"cap-color"] == "c").sum())
print("Poisonous_green:",(poison_df.loc[:,"cap-color"] == "g").sum())
print("Poisonous_buff:",(poison_df.loc[:,"cap-color"] == "b").sum())
print("Poisonous_purple:",(poison_df.loc[:,"cap-color"] == "p").sum())
print("Poisonous_red:",(poison_df.loc[:,"cap-color"] == "e").sum())

"""

edible = mush_df["class"] == "e"
cols = ["class","cap-shape","cap-surface","cap-color","bruises","odor"	,"gill-attachment",	"gill-spacing",	"gill-size",	"gill-color"	,"stalk-shape"	,"stalk-root",	"stalk-surface-above-ring",	"stalk-surface-below-ring",	"stalk-color-above-ring",	"stalk-color-below-ring","veil-type",	"veil-color"	,"ring-number",	"ring-type",	"spore-print-color",	"population","habitat"]
edible_df = mush_df.loc[edible,cols]
display(edible_df)