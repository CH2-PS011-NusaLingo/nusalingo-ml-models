import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import models
from input import voice_input
from transform import preprocess_audiobuffer


# Mengambil Model yang dibutuhkan
loaded_model = models.load_model("sunda_coba1.h5")

# Lbael yang kami miliki
sundas = ['abdi', 'angkat', 'anjeun', 'bingung', 'bungah', 'dimana', 'dongkap', 'hoyong',
 'ieu', 'inuman', 'kadaharan', 'kamana', 'kumaha', 'lapar', 'meuli', 'nginum',
 'pangaos', 'sabaraha', 'tuang', 'wartos']


# Membuat prediksi output
def predict_output():
    audio = voice_input("test_sunda/pangaos_test1.wav")
    spec = preprocess_audiobuffer(audio)
    prediction = loaded_model(spec)
    label_pred = np.argmax(prediction, axis=1)
    sunda = sundas[label_pred[0]]
    prediction = tf.keras.activations.softmax(prediction)
    final_y = prediction[0][label_pred[0]]
    # print("Predicted label:", sunda)
    return sunda, final_y


if __name__ == "__main__":
    while True:
        sunda, final_y = predict_output()
        print(f"Predicted label: {sunda} with probabilities: {final_y}")
        # ... Further processing with probabilities (optional) ...
        break
        # output = predict_output()
        # if output == output :
        #     break