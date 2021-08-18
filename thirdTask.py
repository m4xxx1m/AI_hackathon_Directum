from keras.models import load_model
import numpy as np
import cv2


def third_task(output, image_path):
    model = load_model('keras_model.h5')

    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = cv2.imread(image_path)
    size = (224, 224)
    image = cv2.resize(image, size)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array

    prediction = model.predict(data)
    result = 'other'
    if prediction[0][0] > prediction[0][1]:
        result = 'main'
    output.source.type = result
    return output
