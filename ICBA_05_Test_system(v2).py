#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Test data prediction

# to mount Google Drive
from google.colab import drive
drive.mount('/gdrive')

import tensorflow as tf
tf.__version__

from google.colab import drive
drive.mount('/content/drive')


# In[2]:


# libraries

import pandas as pd
import numpy as np
import os
import keras
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Dense,GlobalAveragePooling2D
from tensorflow.keras.applications import InceptionResNetV2, VGG16, ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam, SGD
from keras.models import load_model


# In[13]:


# Model loading...

classes = ['0', '1', '2', '3', '4', '5']

model_to_use='resnet50'

base_model=ResNet50(weights='imagenet',include_top=False)
for layer in base_model.layers:
    layer.trainable=False

x=base_model.output
x=GlobalAveragePooling2D()(x)
x=Dense(128,activation='relu')(x)
x=Dense(128,activation='relu')(x)
preds=Dense(len(classes),activation='softmax')(x) 

model=Model(inputs=base_model.input, outputs=preds)

# pre-trained model (!)
model_path = '/content/drive/MyDrive/ICBA/Models/model-epoch-002-valacc-0.976103.h5'
model.load_weights(model_path)


# In[15]:


# Image generator for test data

test_save = '/content/drive/MyDrive/ICBA/DataBase/ICBA/f4DL_2020_11_v3/Dataset4DL_v3/test'
print(test_save)

test_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

test_generator=test_datagen.flow_from_directory(test_save, 
                                                target_size=(224,224),
                                                color_mode='rgb',
                                                batch_size=16,
                                                class_mode=None,
                                                shuffle=False)


# In[33]:


# data in order (?)

non_sorted = test_generator.filenames
sorted_list = sorted(non_sorted)

sorted_list == non_sorted


# In[19]:


# Class per each file from test

ytrue_test = np.zeros(len(test_generator.filenames))

c1 = 0
for filenm in test_generator.filenames:
  file1 = filenm
  split = file1.split('/')]
  ytrue_test[c1] = split[0]
  c1 = c1 + 1

print(ytrue_test)
np.bincount(ytrue_test)


# In[22]:


from keras.utils import to_categorical

ypred_test = model.predict_generator(test_generator, steps=len(test_generator))
ypred_labels_test = np.argmax(ypred_test, axis=1)
print(ypred_labels_test)
ypred_onehot_test = to_categorical(ypred_labels_test, num_classes=6)


# In[25]:


from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

confusion_matrix(ytrue_test, ypred_labels_test)


# In[26]:


print(classification_report(ytrue_test, ypred_labels_test))


# In[34]:


# Results.csv

import numpy as np
import pandas as pd

ytrue_test = np.zeros(len(test_generator.filenames), dtype=np.int)

c1 = 0
true_and_predict = np.zeros((len(test_generator.filenames),3), dtype=object)

filenames = test_generator.filenames

for filenm in test_generator.filenames:
  file1 = filenm
  split = file1.split('/')
  
  true = split[0]
  predict = np.argmax(ypred_test[c1])
  
  true_and_predict[c1,0] = filenm
  true_and_predict[c1,1] = true
  true_and_predict[c1,2] = predict
  c1 = c1 + 1

df = pd.DataFrame(true_and_predict,  columns=['class / filename','ytrue_test','ypredict_test'])
df.to_csv("results.csv")
print(df)

