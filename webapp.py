import os
from flask import Flask, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
import numpy as np
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
from icba_predictions import icba_diseases_list, icba_html_predictions
from icba_predictions_fr import icba_html_predictions_fr
from icba_predictions_ar import icba_html_predictions_ar
import cv2
import math

app = Flask(__name__)

@app.route('/', methods=['GET'])
def render_main_page():
    return render_template('index.html')

@app.route('/privacy', methods=['GET'])
def render_privacy_page():
    return render_template('privacy-policy.html')

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
icba_preds = Dense(21, activation='softmax')(icba_x)

icba_model = Model(inputs=icba_base_model.input, outputs=icba_preds)

icba_model_path = 'static/models/icba/model-epoch-039-valacc-0.914187.h5'
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

def get_index_with_offset(i, ptype):
#   if ptype == 1:
#     return i
#   elif ptype == 2:
#     return i+5
#   elif ptype == 3:
#     return i+12
#   elif ptype == 4:
#     return i+20
  return i

def validate_confidence(c, i, ptype):
  if ptype == 1 and i > 4:
    return 0
  elif ptype == 2 and (i < 5 or i > 11):
    return 0
  elif ptype == 3 and (i < 12 or i > 19):
    return 0
  elif ptype == 4 and i < 20:
    return 0
  return c

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
def render_icba_predict_no_ptype(filename):
    return render_icba_predict(filename, 0)

@app.route('/icba/predict/<filename>/<ptype>')
def render_icba_predict(filename, ptype):
    result = icba_predict(filename)
    i = result.get('index')
    c = result.get('confidence')

    if i < 0:
        return render_template('icba/error.html', message=result.get('errorMsg'))

    index = get_index_with_offset(i, ptype)
    c = validate_confidence(c, index, ptype)
    return render_template('icba/result.html', predictions=icba_html_predictions[index], confidence=c)

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
def icba_api_predict_no_ptype(filename):
    return icba_api_predict(filename, 0)

@app.route('/api/predict/<filename>/<ptype>')
def icba_api_predict(filename, ptype):
    result = icba_predict(filename)
    i = result.get('index')
    c = result.get('confidence')

    if i < 0:
        return jsonify(success=0, message=result.get('errorMsg'))

    index = get_index_with_offset(i, ptype)
    c = validate_confidence(c, index, ptype)
    return jsonify(success=1, disease=icba_diseases_list[index], confidence=c)

@app.route('/api/diseases')
def icba_diseases():
    return jsonify(success=1, diseases=icba_diseases_list)

# ----------------------------------------------------------

# ----------------------------------------------------------
# ICBA FR
# ----------------------------------------------------------

@app.route('/icbafr', methods=['GET', 'POST'])
def render_icbafr_main_page():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        if not filename:
            return render_template('icbafr/error.html', message="Veuillez sélectionner un fichier à classer")
        file.save(os.path.join('uploads', filename))
        return redirect(url_for('render_icbafr_predict', filename=filename))
    return render_template('icbafr/index.html')

@app.route('/icbafr/predict/<filename>')
def render_icbafr_predict_no_ptype(filename):
    return render_icbafr_predict(filename, 0)

@app.route('/icbafr/predict/<filename>/<ptype>')
def render_icbafr_predict(filename, ptype):
    result = icba_predict(filename)
    i = result.get('index')
    c = result.get('confidence')

    if i < 0:
        return render_template('icbafr/error.html', message=result.get('errorMsg'))

    index = get_index_with_offset(i, ptype)
    c = validate_confidence(c, index, ptype)
    return render_template('icbafr/result.html', predictions=icba_html_predictions_fr[index], confidence=c)

@app.route('/icbafr/diseases')
def render_icbafr_diseases():
    return render_template('icbafr/diseases.html', predictions=icba_html_predictions_fr)

# ----------------------------------------------------------

# ----------------------------------------------------------
# ICBA AR
# ----------------------------------------------------------

@app.route('/icbaar', methods=['GET', 'POST'])
def render_icbaar_main_page():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        if not filename:
            return render_template('icbaar/error.html', message="الرجاء تحديد ملف لتصنيفه")
        file.save(os.path.join('uploads', filename))
        return redirect(url_for('render_icbaar_predict', filename=filename))
    return render_template('icbaar/index.html')

@app.route('/icbaar/predict/<filename>')
def render_icbaar_predict_no_ptype(filename):
    return render_icbaar_predict(filename, 0)

@app.route('/icbaar/predict/<filename>/<ptype>')
def render_icbaar_predict(filename, ptype):
    result = icba_predict(filename)
    i = result.get('index')
    c = result.get('confidence')

    if i < 0:
        return render_template('icbaar/error.html', message=result.get('errorMsg'))

    index = get_index_with_offset(i, ptype)
    c = validate_confidence(c, index, ptype)
    return render_template('icbaar/result.html', predictions=icba_html_predictions_ar[index], confidence=c)

@app.route('/icbaar/diseases')
def render_icbaar_diseases():
    return render_template('icbaar/diseases.html', predictions=icba_html_predictions_ar)

# ----------------------------------------------------------
