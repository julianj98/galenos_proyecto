from keras.applications.imagenet_utils import preprocess_input
from keras.models import load_model
from skimage.color import rgb2gray
from keras.preprocessing import image
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras import datasets, layers, models



def diagnostico(path_image):
    width_shape = 150
    height_shape = 150

    names = ['NEUMONIA', "NO NEUMONIA"]
 
    imaget_path = path_image[1:]

    path_model = 'IA/modelo.h5'
    new_model = load_model(path_model)
    modelt=new_model

 

    img=tf.keras.preprocessing.image.load_img(imaget_path, target_size=(150,150,3))
    x=image.img_to_array(img)
    x= cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
    x=np.expand_dims(x, axis=0)
    images = np.vstack([x])
    images = images.reshape(-1, 150, 150, 1)


    preds = modelt.predict(images, batch_size=10)


    
    #plt.axis('off')
  

    array_neumonia=[0., 1.]
    array_normal=[1., 0.]

    b = np.array([0, 1])
    c = np.less_equal(preds, b)

    if (c== True).all() :
        resultado="NEUMONIA"
    else:
        resultado="NORMAL"
        
    return resultado



#plt.imshow(img)