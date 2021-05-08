import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import numpy as np
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
import cv2
import math

app = Flask(__name__)

classes = ['0', '1', '2', '3', '4', '5']
predictions = [
    {
        'title': 'Cucumber',
        'type': 'Sucking Insect',
        'disease': 'Spider Mite',
        'sci': 'Tetranychus spp.',
        'hosts': 'Wide range of garden plants, including many vegetables (e.g., beans, eggplant), fruits (e.g., raspberries, currants, pear) and flowers.',
        'symptoms': '''<ul>
            <li>Tiny insects usually found on the back of leaves.</li>
            <li>Range in color from red and brown to yellow and green</li>
            <li>Produce webbing, when occur in high population, similar to the spiders</li>
            <li>Infected leaves appear discolored with pale dots, become scorched and drop.</li>
        </ul>''',
        'control': '''<ul>
            <li>Spray Dicofol 18.5 EC @ 2000 ml/ha</li>
        </ul>''',
        'image': 'images/0.jpg'
    },
    {
        'title': 'Cucumber',
        'type': 'Fungal Disease',
        'disease': 'Downy Mildew',
        'sci': 'Pseudoperonospora spp.',
        'hosts': 'Many common vegetables including brassicas (cabbage, cauliflower, mustard), carrot, lettuce, onion, spinach, beans, cucumber and cantaloupes',
        'symptoms': '''<ul>
            <li>Angular, pale yellow patches delineated by leaf veins.</li>
            <li>Mold-like growth on the underside of the leaf, corresponding to the blotch on the upper surface.</li>
            <li>Plants stunted, lack vigor, and die.</li>
        </ul>''',
        'control': '''<ul>
            <li>Seed treatment with (Carboxyn 37.5% + Thiram 37.5% ) or Carbendazim  DS @ 1.5 g/kg of seeds</li>
            <li>Spray Mancozeb 0.25% or Matalaxyl 0.15%</li>
        </ul>''',
        'image': 'images/1.jpg'
    },
    {
        'title': 'Cucumber',
        'type': 'Potassium (K)',
        'disease': 'Nutrient Deficiency',
        'sci': '',
        'hosts': '',
        'symptoms': '''<ul>
            <li>Older leaves may wilt, look scorched.</li>
            <li>Interveinal chlorosis begins at the base, scorching inward from leaf margins.</li>
        </ul>''',
        'control': '',
        'image': 'images/2.jpg'
    },
    {
        'title': 'Tomato',
        'type': 'Fungal Disease',
        'disease': 'Powdery Mildew',
        'sci': '''Erysiphe spp.
        Sphaerotheca spp.''',
        'hosts': 'Affect all kinds of plants: cereals and grasses, vegetables, ornamentals and fruit trees, broad-leaved shade and forest trees',
        'symptoms': '''<ul>
            <li>Spots or patches of white to grayish, talcum-powder like growth - mostly on the upper sides of the leaves.</li>
            <li>Can also affect the bottom sides of leaves, young stems, buds, flowers, and young fruit.</li>
        </ul>''',
        'control': '''<ul>
            <li>Spary Dinocap 0.2% or Tridemorph 0.1% or Chlorothalonil 0.15% or Hexaconazole 0.1% or Wettable sulphur 0.3%</li>
        </ul>''',
        'image': 'images/3.jpg'
    },
    {
        'title': 'Pepper',
        'type': 'Fungal Disease',
        'disease': 'Downy Mildew',
        'sci': 'Pseudoperonospora spp.',
        'hosts': 'Many common vegetables including brassicas (cabbage, cauliflower, mustard), carrot, lettuce, onion, spinach, beans, cucumber and cantaloupes',
        'symptoms': '''<ul>
            <li>Angular, pale yellow patches delineated by leaf veins.</li>
            <li>Mold-like growth on the underside of the leaf, corresponding to the blotch on the upper surface.</li>
            <li>Plants stunted, lack vigor, and die.</li>
        </ul>''',
        'control': '''<ul>
            <li>Seed treatment with (Carboxyn 37.5% + Thiram 37.5% ) or Carbendazim  DS @ 1.5 g/kg of seeds</li>
            <li>Spray Mancozeb 0.25% or Matalaxyl 0.15%</li>
        </ul>''',
        'image': 'images/4.jpg'
    },
    {
        'title': 'Pepper',
        'type': 'Sucking Insect',
        'disease': 'Spider Mite',
        'sci': 'Tetranychus spp.',
        'hosts': 'Wide range of garden plants, including many vegetables (e.g., beans, eggplant), fruits (e.g., raspberries, currants, pear) and flowers.',
        'symptoms': '''<ul>
            <li>Tiny insects usually found on the back of leaves.</li>
            <li>Range in color from red and brown to yellow and green.</li>
            <li>Produce webbing, when occur in high population, similar to the spiders.</li>
            <li>Infected leaves appear discolored with pale dots, become scorched and drop.</li>
        </ul>''',
        'control': '''<ul>
            <li>Spray Dicofol 18.5 EC @ 2000 ml/ha</li>
        </ul>''',
        'image': 'images/5.jpg'
    },
]

base_model = ResNet50(weights='imagenet', include_top=False)
for layer in base_model.layers:
    layer.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
x = Dense(128, activation='relu')(x)
preds = Dense(len(classes), activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=preds)

model_path = 'model-epoch-002-valacc-0.976103.h5'
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


app.run(host='0.0.0.0', port=2000)
