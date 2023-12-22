# File : Main.py

import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import models
from input import voice_input
from transform import preprocess_audiobuffer


# Mengambil Model yang dibutuhkan
loaded_model = models.load_model("Sunda/sunda_coba1.h5")

# Label yang kami miliki
sundas = ['inuman', 'bingung', 'anjeun', 'dongkap', 'ieu', 'bungah', 'angkat', 'hoyong',
 'dimana', 'abdi', 'pangaos', 'nginum', 'wartos', 'sabaraha', 'kadaharan',
 'meuli', 'kamana', 'tuang', 'lapar', 'kumaha']

# Membuat prediksi output
def predict_output_sunda(filename):
    audio_data = voice_input(filename)
    spec = preprocess_audiobuffer(audio_data)
    prediction = loaded_model(spec)
    label_pred = np.argmax(prediction, axis=1)
    sunda = sundas[label_pred[0]]
    prediction = tf.keras.activations.softmax(prediction)
    final_y = prediction[0][label_pred[0]]
    # print("Predicted label:", sunda)
    return sunda, final_y


if __name__ == "__main__":
    while True:
        filename = "test_sunda/test2.wav"
        sunda, final_y = predict_output_sunda(filename)
        print(f"Predicted label: {sunda} with probabilities: {final_y}")
        # ... Further processing with probabilities (optional) ...
        break
        # output = predict_output()
        # if output == output :
        #     break