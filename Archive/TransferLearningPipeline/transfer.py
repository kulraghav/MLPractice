
"""
    This module provides basic functions to facilitate 
    transfer learning on images.
"""

import numpy as np
from PIL import Image

from keras.applications.resnet50 import ResNet50, preprocess_input


resnet_model = ResNet50(weights='imagenet', include_top=False, input_shape=(200, 200, 3))

def get_vector(image_path, model=resnet_model):
    image = Image.open(image_path)

    resized_image = image.resize((200, 200), Image.NEAREST)
    resized_image.load()

    resized_image = np.asarray(resized_image, dtype="uint8")
    X = np.array([resized_image]).astype('float32')
    resnet_input = preprocess_input(X)

    last_layer_activations = model.predict(resnet_input)

    vector = last_layer_activations.reshape(1, 2048)

    return vector
