from keras.models import load_model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model

# ----------------------------------------------------------
# Base model
# input: numclass -> number of output class
# output: model -> the model base created
# ----------------------------------------------------------
def create_base_model(numclass):
    base_model = ResNet50(weights='imagenet', include_top=False)
    for layer in base_model.layers:
        layer.trainable = False

    output = base_model.output
    output = GlobalAveragePooling2D()(output)
    output = Dense(128, activation='relu')(output)
    output = Dense(128, activation='relu')(output)
    preds = Dense(numclass, activation='softmax')(output)

    model = Model(inputs= base_model.input, outputs=preds)

    return model

# ----------------------------------------------------------
# Load the weights (h5 file) to the model base
# input: model ->(model base created with create_base_model
#        and weights_fileh5 -> the file h5 with the weights 
#                              of respective model
# output: model -> model with the weights load
# ----------------------------------------------------------
def load_weights_model(model, weights_fileh5):
    model.load_weights(weights_fileh5)
    return model

# ----------------------------------------------------------
# get the summary of the model architecture
# input: weights_fileh5 -> the file h5 with the weights 
#                          of respective model
# output: architecture -> model architecture summary
# ----------------------------------------------------------
def summary_architecture(weights_fileh5):
    # Cargar modelo desde archivo .h5
    model = load_model(weights_fileh5)
    architecture = model.summary()
    return architecture

# ----------------------------------------------------------
# get the model weights load
# input: model -> the model
# output: weights -> model weights load
# ----------------------------------------------------------
def getweights(model):
    # Obtener pesos del modelo
    weights = model.get_weights()
    return weights