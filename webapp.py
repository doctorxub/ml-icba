import os
from flask import Flask, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
import numpy as np
from mrcnn import model as modellib, utils, visualize
from mrcnn.config import Config
import matplotlib.pyplot as plt
import json
import skimage
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
from icba_predictions import icba_diseases_list, icba_html_predictions
from ctfc_predictions import ctfc_diseases_list, ctfc_html_predictions
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

# ----------------------------------------------------------
# CTFC
# ----------------------------------------------------------
tag_name = 'conepines'

class PineConfig(Config):
    NAME = tag_name
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    NUM_CLASSES = 1 + 1  # Background + 1 (Conepine)
    IMAGE_RESIZE_MODE = "crop"
    IMAGE_MIN_DIM = 512
    IMAGE_MAX_DIM = 512
    IMAGE_MIN_SCALE = 2.0
    DETECTION_MIN_CONFIDENCE = 0
    STEPS_PER_EPOCH = 500
    VALIDATION_STEPS = 5
    BACKBONE = 'resnet50'
    RPN_ANCHOR_SCALES = (8, 16, 32, 64, 128)
    TRAIN_ROIS_PER_IMAGE = 128
    MAX_GT_INSTANCES = 500
    POST_NMS_ROIS_INFERENCE = 2000 
    POST_NMS_ROIS_TRAINING = 1000
    RPN_NMS_THRESHOLD = 0.9
    RPN_TRAIN_ANCHORS_PER_IMAGE = 64
    MEAN_PIXEL = np.array([43.53, 39.56, 48.22])
    USE_MINI_MASK = True
    MINI_MASK_SHAPE = (56, 56) # (height, width) of the mini-mask -It doesn't change-
    DETECTION_MAX_INSTANCES = 1000    

config = PineConfig()
config.display()

class InferenceConfig(PineConfig):
    IMAGE_RESIZE_MODE = "pad64"
    RPN_NMS_THRESHOLD = 0.7

inference_config = InferenceConfig()
inference_config.display()

ctfc_model_path = 'static/models/ctfc/model_v1.h5'
ctfc_data_dir = 'data'
model = modellib.MaskRCNN(mode="inference", config=inference_config, model_dir=ctfc_data_dir)
model.load_weights(ctfc_model_path, by_name=True)

def ctfc_predict(filename):
    result = {'index': -1, 'errorMsg': ''}

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

        result = model.detect([img], verbose=0)[0]
        print(result)
        result['index'] = 1
        os.remove(file_path)
    
    if result['index'] < 0:
        result['errorMsg'] = "This file no longer exists"

    return result
@app.route('/ctfc', methods=['GET', 'POST'])
def render_ctfc_main_page():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        if not filename:
            return render_template('ctfc/error.html', message="Please select a file to classify")
        file.save(os.path.join('uploads', filename))
        return redirect(url_for('render_ctfc_predict', filename=filename))
    return render_template('ctfc/index.html')

@app.route('/ctfc/predict/<filename>')
def render_ctfc_predict(filename):
    result = ctfc_predict(filename)
    i = result.get('index')

    if i < 0:
        return render_template('ctfc/error.html', message=result.get('errorMsg'))
    return render_template('ctfc/result.html', predictions=result)

@app.route('/api/ctfc/upload', methods=['POST'])
def ctfc_upload_image():
    file = request.files['file']
    filename = secure_filename(file.filename)
    if not filename:
        return jsonify(success=0, message='Please select a file to classify')
    file.save(os.path.join('uploads', filename))
    return jsonify(success=1, filename=filename)

@app.route('/api/ctfc/predict/<filename>')
def ctfc_api_predict(filename):
    result = ctfc_predict(filename)
    i = result.get('index')

    if i < 0:
        return jsonify(success=0, message=result.get('errorMsg'))
    return jsonify(success=1, result=result)
# ----------------------------------------------------------
