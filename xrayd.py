from functools import partial
from tensorflow.python.framework import tensor_conversion_registry 
from tensorflow.keras import models
import numpy as np
from tensorflow.keras.preprocessing import image
import tensorflow as tf
gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.333)
sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options))
model = models.load_model("final/models/model_final_100v2.hdf5")
def classify(filename):
    tf.compat.v1.keras.backend.set_session(sess)
    imgpath=filename# set the image path
    print(imgpath)
    img = image.load_img(imgpath, target_size=(224, 224),color_mode = "grayscale")
    img = image.img_to_array(img)           
    img = np.expand_dims(img, axis=0)         
    #img /= 255.                                     
    pred = model.predict(img)
    index = np.argmax(pred)
    class_list=['normal','pneumonia','covid']
    class_list.sort()
    pred_value = class_list[index]
    k = 3
    confidences = np.squeeze(model.predict(img))
    classs = np.argmax(confidences)
    top_conf  = confidences[classs]
    top_conf = top_conf*100
    top_conf = float("{:.5f}".format(top_conf))
    #print(pred_value)
    return pred_value, top_conf