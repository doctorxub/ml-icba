import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename


app = Flask(__name__)

from tensorflow.keras.models import load_model
from skimage.transform import resize
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np


from tensorflow.keras.layers import Dense,GlobalAveragePooling2D
from tensorflow.keras.applications import InceptionResNetV2, VGG16, ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam, SGD
from tensorflow.keras.utils import to_categorical
import sys


global model_to_use
global classes
global base_model
global x
global preds

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

model_path = 'model-epoch-002-valacc-0.976103.h5'
model.load_weights(model_path)

print("Loading model")
global sess
sess = tf.compat.v1.Session()
tf.compat.v1.keras.backend.set_session(sess)
global graph
graph = tf.compat.v1.get_default_graph()

@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))
        return redirect(url_for('prediction', filename=filename))
    return render_template('index.html')

@app.route('/prediction/<filename>')
def prediction(filename):
    img = plt.imread(os.path.join('uploads', filename))
    img_resized = resize(img, (224,224))
    img_reshaped = np.reshape(img_resized, [1, 224, 224, 3])
    classes = model.predict(img_reshaped, batch_size=1)
    print ('Model prediction:')
    print(np.round(classes))

    max_index = np.argmax(classes, axis=1)
    print("class number: ")
    print(max_index)

    #Step 5
    return render_template('temp.html', predictions=max_index)

app.run(host='0.0.0.0', port=2000)
