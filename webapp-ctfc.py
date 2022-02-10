import os
from flask import Flask, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
import numpy as np
from mrcnn import model as modellib
from mrcnn.config import Config
import cv2

app = Flask(__name__)

@app.route('/', methods=['GET'])
def render_main_page():
    return render_template('index.html')

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
