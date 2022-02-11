import os
from flask import Flask, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
import numpy as np
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
from icba_predictions import icba_diseases_list, icba_html_predictions
import cv2
import math

app = Flask(__name__)

@app.route('/', methods=['GET'])
def render_main_page():
    return render_template('index.html')

# ----------------------------------------------------------
# ICBA
# ----------------------------------------------------------
icba_base_model = ResNet50(weights='imagenet', include_top=False)
for layer in icba_base_model.layers:
    layer.trainable = False

icba_x = icba_base_model.output
icba_x = GlobalAveragePooling2D()(icba_x)
icba_x = Dense(128, activation='relu')(icba_x)
icba_x = Dense(128, activation='relu')(icba_x)
icba_preds = Dense(9, activation='softmax')(icba_x)

icba_model = Model(inputs=icba_base_model.input, outputs=icba_preds)

icba_model_path = 'static/models/icba/2021-06-model-epoch-007-valacc-0.974116.h5'
icba_model.load_weights(icba_model_path)

def icba_predict(filename):
    result = {'index': -1, 'confidence': 0, 'errorMsg': ''}

    if not filename:
        result['errorMsg'] = "Please select a file to classify"
        return result

    file_path = os.path.join('uploads', filename)

    if os.path.exists(file_path):
        img = cv2.imread(file_path)
        if img is None or img.size == 0:
            os.remove(file_path)
            result['errorMsg'] = "Unsupported format"
            return result
        img = cv2.resize(img, (224, 224))
        img = np.reshape(img, [1, 224, 224, 3])
        classes = icba_model.predict(img, batch_size=1)
        max_index = np.argmax(classes, axis=1)
        result['index'] = max_index[0]
        result['confidence'] = math.floor(np.amax(classes) * 100)
        os.remove(file_path)
    
    if result['index'] < 0:
        result['errorMsg'] = "This file no longer exists"

    return result

@app.route('/icba', methods=['GET', 'POST'])
def render_icba_main_page():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        if not filename:
            return render_template('icba/error.html', message="Please select a file to classify")
        file.save(os.path.join('uploads', filename))
        return redirect(url_for('render_icba_predict', filename=filename))
    return render_template('icba/index.html')

@app.route('/icba/predict/<filename>')
def render_icba_predict(filename):
    result = icba_predict(filename)
    i = result.get('index')
    c = result.get('confidence')

    if i < 0:
        return render_template('icba/error.html', message=result.get('errorMsg'))
    return render_template('icba/result.html', predictions=icba_html_predictions[i], confidence=c)

@app.route('/icba/diseases')
def render_icba_diseases():
    return render_template('icba/diseases.html', predictions=icba_html_predictions)

@app.route('/api/upload', methods=['POST'])
def icba_upload_image():
    file = request.files['file']
    filename = secure_filename(file.filename)
    if not filename:
        return jsonify(success=0, message='Please select a file to classify')
    file.save(os.path.join('uploads', filename))
    return jsonify(success=1, filename=filename)

@app.route('/api/predict/<filename>')
def icba_api_predict(filename):
    result = icba_predict(filename)
    i = result.get('index')
    c = result.get('confidence')

    if i < 0:
        return jsonify(success=0, message=result.get('errorMsg'))
    return jsonify(success=1, disease=icba_diseases_list[i], confidence=c)

@app.route('/api/diseases')
def icba_diseases():
    return jsonify(success=1, diseases=icba_diseases_list)
# ----------------------------------------------------------
