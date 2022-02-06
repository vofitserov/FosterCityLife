import numpy as np
import os
import time
import ssl

os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
ssl._create_default_https_context = ssl._create_unverified_context

from config import *
# Named global logger from config
logger = logging.getLogger("fostercitylife")

import keras
import keras.applications as kapp
from keras.applications.vgg19 import preprocess_input
from keras.applications.vgg19 import decode_predictions

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array

import mtcnn

class ImageAnalyser:
    def __init__(self):
        self.detector = mtcnn.MTCNN()
        logger.info("initializing vgg19...")
        self.model = kapp.VGG19()
        self.model.compile(optimizer='sgd', loss='categorical_crossentropy',
              metrics=['accuracy'])
        logger.info("vgg19 compiled.")
        return

    def predict(self, imagefile):
        logger.info("preprocessing %s" % imagefile)
        # load image from the file
        image = load_img(imagefile, target_size=(224,224))
        # convert the image pixels to a numpy array
        image_a = img_to_array(image)
        # reshape data for the model
        image = image_a.reshape((1, image_a.shape[0], image_a.shape[1], image_a.shape[2]))
        # prepare the image for the VGG model
        image = preprocess_input(image)
        logger.info("running object prediction...")
        yhat = self.model.predict(image)
        # convert the probabilities to class labels
        labels = decode_predictions(yhat, top=10)

        logger.info("running face prediction...")
        faces = self.detector.detect_faces(image_a)
        if len(faces) > 0:
            logger.info("face detected: %s" % str(faces[0]))
            labels[0].append((str(faces[0]["box"]), 'face', faces[0]["confidence"]))
        else:
            logger.info("no face detected.")
        logger.info("predicted: %s" % str(labels))
        return labels[0]

def main(argv):
    analyzer = ImageAnalyser()
    imagefile_1 = "db/1345167670677827586_134465215_456210729105910_3001387490591961883_n.jpg"
    analyzer.predict(imagefile_1)
    imagefile_2 = "db/1344857801026392065_134560718_696640641220281_2246675343671407131_n.jpg"
    analyzer.predict(imagefile_2)
    return

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main(sys.argv)
