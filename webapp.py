import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import numpy as np
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
from predictions import predictions, classes
import cv2
import math

app = Flask(__name__)

base_model = ResNet50(weights='imagenet', include_top=False)
for layer in base_model.layers:
    layer.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
x = Dense(128, activation='relu')(x)
preds = Dense(len(classes), activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=preds)

model_path = '2021-06-model-epoch-007-valacc-0.974116.h5'
model.load_weights(model_path)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        if not filename:
            return render_template('error.html', message="Please select a file to classify")
        file.save(os.path.join('uploads', filename))
        return redirect(url_for('prediction', filename=filename))
    return render_template('index.html')


@app.route('/prediction/<filename>')
def prediction(filename):
    if not filename:
        return render_template('error.html', message="Please select a file to classify")
    file_path = os.path.join('uploads', filename)
    index = -1
    if os.path.exists(file_path):
        img = cv2.imread(file_path)
        if img is None or img.size == 0:
            os.remove(file_path)
            return render_template('error.html', message="Unsupported format")
        img = cv2.resize(img, (224, 224))
        img = np.reshape(img, [1, 224, 224, 3])
        classes = model.predict(img, batch_size=1)
        max_index = np.argmax(classes, axis=1)
        index = max_index[0]
        confidence = math.floor(np.amax(classes) * 100)
        os.remove(file_path)
    if index >= 0:
        return render_template('result.html', predictions=predictions[index], confidence=confidence)
    else:
        return render_template('error.html', message="This file no longer exists")


@app.route('/diseases')
def diseases():
    return render_template('diseases.html', predictions=predictions)


app.run(host='0.0.0.0', port=2000)
