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

# This line was added for this version
from readingModelArch import load_weights_model, create_base_model

app = Flask(__name__)

url_base =  'https://doctorxub.com'
#url_base = 'https://79c5-181-55-68-32.ngrok-free.app'
url_en = url_base + '/icba'
url_fr = url_base + '/icbafr'
url_ar = url_base + '/icbaar'

#-------------------------------------
# location of h5 files for each model
#-------------------------------------
icba_model_path_cucumber = 'static/models/icba/model_v2_cucumber-epoch-012-valacc-0.982738.h5'
icba_model_path_tomato = 'static/models/icba/model_v2_tomato-epoch-068-valacc-0.953786.h5'
icba_model_path_pepper = 'static/models/icba/model_v2_pepper-epoch-058-valacc-0.951003.h5'

@app.route('/', methods=['GET'])
def render_main_page():  
    return render_template('index.html', url_en=url_en, url_fr=url_fr, url_ar=url_ar)


@app.route('/privacy', methods=['GET'])
def render_privacy_page():
    return render_template('privacy-policy.html')

# ----------------------------------------------------------
# ICBA Base model|
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


icba_model_cucumber = create_base_model(5)
icba_model_cucumber = load_weights_model(icba_model_cucumber, icba_model_path_cucumber)

icba_model_tomato = create_base_model(7)
icba_model_tomato = load_weights_model(icba_model_tomato, icba_model_path_tomato)

icba_model_pepper = create_base_model(7)
icba_model_pepper = load_weights_model(icba_model_pepper, icba_model_path_pepper)

#------------------------------------------------------------------------
# This method calls the respective model
# input: filename -> image file name
#        ptype -> crop type
#        ptype = 0 : modelo full diseases including Cucumber, pepper and 
#                    tomato, default value is 0
#        ptype = 1 : Cucumber
#        ptype = 2 : Pepper
#        ptype = 3 : tomato
# output: result -> a dict with the 'index' in the database of the disease 
#                   predicted. -1 if there was an error predicting
#                   'confidence' of the prediction and 'errorMsg' in case
#                   of an error ocurr
#-------------------------------------------------------------------------
def icba_predict(filename, ptype=""):
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
        
        if (ptype == "cucumber"):
            # ptype = 1 : Cucumber
            classes = icba_model_cucumber.predict(img, batch_size=1)
        elif (ptype == "capsicum"):
            # ptype = 2 : Pepper
            classes = icba_model_pepper.predict(img, batch_size=1)
        elif (ptype == "tomato"):
            # ptype = 3 : tomato
            classes = icba_model_tomato.predict(img, batch_size=1)
        else:
            # ptype = 0 : modelo full diseases including Cucumber, pepper and tomato
            classes = icba_model.predict(img, batch_size=1)

        max_index = np.argmax(classes, axis=1)
        result['index'] = max_index[0]
        result['confidence'] = math.floor(np.amax(classes) * 100)
       
        os.remove(file_path)
    
    if result['index'] < 0:
        result['errorMsg'] = "This file no longer exists"

    return result


#------------------------------------------------------------------------
# This method geet the resective index from the database for the 
# corresponding disease predicted
# input: i -> the index of the disease predicted
#        ptype -> crop type
#        ptype = 0 : modelo full diseases including Cucumber, pepper and 
#                    tomato
#        ptype = 1 : Cucumber
#        ptype = 2 : Pepper
#        ptype = 3 : tomato
# output: i -> the index with offset from the list of diseases corresponding 
#              with the predicted
#-------------------------------------------------------------------------
def get_index_with_offset(i, ptype=0):
   if ptype == 1:
     return i # This first 5 correspond with cucumber
   elif ptype == 2:
     return i+5 # Skip 5 from cucumber for pepper
   elif ptype == 3:
     return i+12 # Skip 5 from cucumber + 7 from pepper
   return i


def validate_confidence(c, i, ptype):
  if ptype == 1 and i > 4:
    return 0
  elif ptype == 2 and (i < 5 or i > 11):
    return 0
  elif ptype == 3 and (i < 12 or i > 20):
    return 0
  elif ptype == 4 and (i < 20):
    return 0
  return c


@app.route('/icba', methods=['GET', 'POST'])
def render_icba_main_page():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        if not filename:
            return render_template('icba/error.html', 
                                   message="Please select a file to classify", 
                                   url_x=url_en)
        file.save(os.path.join('uploads', filename))
        # leer ptype del campo de entrada oculto
        ptype = request.form.get('ptype', 0)
        return redirect(url_for('render_icba_predict', 
                                filename=filename, 
                                ptype=ptype))
    return render_template('icba/index.html', 
                           url_en=url_en, 
                           url_fr=url_fr, 
                           url_ar=url_ar)


@app.route('/icba/predict/<filename>')
def render_icba_predict_no_ptype(filename):
    return render_icba_predict(filename, 0)

# ptype = 0 : modelo full diseases including Cucumber, pepper and tomato
# ptype = 1 : Cucumber
# ptype = 2 : Pepper
# ptype = 3 : tomato
@app.route('/icba/predict/<filename>/<ptype>')
def render_icba_predict(filename, ptype):
    plant_type = int(ptype)
    result = icba_predict(filename, plant_type)
    i = result.get('index')
    c = result.get('confidence')

    if i < 0:
        return render_template('icba/error.html', 
                               message=result.get('errorMsg'), 
                               url_x=url_en)

    index = get_index_with_offset(i, plant_type)
    c = validate_confidence(c, index, plant_type)
    return render_template('icba/result.html', 
                           predictions=icba_html_predictions[index], 
                           confidence=c, 
                           url_x=url_en)

@app.route('/icba/diseases')
def render_icba_diseases():
    return render_template('icba/diseases.html', 
                           predictions=icba_html_predictions, 
                           url_x=url_en)

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
    return icba_api_predict(filename, "")

#------------------------------------------------------------------------
# This method return a json file with the rediction result
# input: filename -> image file name
#        ptype -> crop type
#        ptype = 0 : modelo full diseases including Cucumber, pepper and 
#                    tomato
#        ptype = 1 : Cucumber
#        ptype = 2 : Pepper
#        ptype = 3 : tomato
# output: json containing the respective disease predicted in details
#-------------------------------------------------------------------------
@app.route('/api/predict/<filename>/<crop>')
def icba_api_predict(filename, crop):
    plant_type = 0
    
    if crop == "tomato":
       plant_type = 3
    elif crop == "cucumber":
       plant_type = 1
    elif crop == "capsicum":
       plant_type = 2
    else:
       result['errorMsg'] = 'Unable to provide a response at the moment. Please check your input and try again'
       return jsonify(success=0, message=result.get('errorMsg'))

    result = icba_predict(filename, crop)
    i = result.get('index')
    c = result.get('confidence')

    if i < 0:
        return jsonify(success=0, message=result.get('errorMsg'))
    
    index = get_index_with_offset(i, plant_type)
    c = validate_confidence(c, index, plant_type)
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
            return render_template('icbafr/error.html', 
                                   message="Veuillez sélectionner un fichier à classer", 
                                   url_x=url_fr)
        ptype = request.form.get('ptype', 0)
        file.save(os.path.join('uploads', filename))
        return redirect(url_for('render_icbafr_predict', 
                                filename=filename, 
                                ptype=ptype))
    return render_template('icbafr/index.html', 
                           url_en=url_en, 
                           url_fr=url_fr, 
                           url_ar=url_ar)

@app.route('/icbafr/predict/<filename>')
def render_icbafr_predict_no_ptype(filename):
    return render_icbafr_predict(filename, 0)

# ptype = 0 : modelo full diseases including Cucumber, pepper and tomato
# ptype = 1 : Cucumber
# ptype = 2 : Pepper
# ptype = 3 : tomato
@app.route('/icbafr/predict/<filename>/<ptype>')
def render_icbafr_predict(filename, ptype):
    plant_type = int(ptype)
    result = icba_predict(filename, plant_type)
    i = result.get('index')
    c = result.get('confidence')

    if i < 0:
        return render_template('icbafr/error.html', 
                               message=result.get('errorMsg'),
                               url_x=url_fr)

    index = get_index_with_offset(i, plant_type)
    c = validate_confidence(c, index, plant_type)
    return render_template('icbafr/result.html', predictions=icba_html_predictions_fr[index], confidence=c, url_en=url_en, url_fr=url_fr, url_ar=url_ar)

@app.route('/icbafr/diseases')
def render_icbafr_diseases():
    return render_template('icbafr/diseases.html', 
                           predictions=icba_html_predictions_fr, 
                           url_x=url_fr)

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
            return render_template('icbaar/error.html', 
                                   message="الرجاء تحديد ملف لتصنيفه", 
                                   url_x=url_ar)
        file.save(os.path.join('uploads', filename))
        # leer ptype del campo de entrada oculto
        ptype = request.form.get('ptype', 0)

        return redirect(url_for('render_icbaar_predict', 
                                filename=filename, 
                                ptype=ptype))
    return render_template('icbaar/index.html', 
                           url_en=url_en, 
                           url_fr=url_fr, 
                           url_ar=url_ar)

@app.route('/icbaar/predict/<filename>')
def render_icbaar_predict_no_ptype(filename):
    return render_icbaar_predict(filename, 0)

@app.route('/icbaar/predict/<filename>/<ptype>')
def render_icbaar_predict(filename, ptype):
    plant_type = int(ptype)
    result = icba_predict(filename, plant_type)
    i = result.get('index')
    c = result.get('confidence')

    if i < 0:
        return render_template('icbaar/error.html', 
                               message=result.get('errorMsg'), 
                               url_x=url_ar)

    index = get_index_with_offset(i, plant_type)
    c = validate_confidence(c, index, plant_type)
    return render_template('icbaar/result.html', 
                           predictions=icba_html_predictions_ar[index], 
                           confidence=c, 
                           url_x=url_ar)

@app.route('/icbaar/diseases')
def render_icbaar_diseases():
    return render_template('icbaar/diseases.html', 
                           predictions=icba_html_predictions_ar, 
                           url_x=url_ar)

# ----------------------------------------------------------


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9095)