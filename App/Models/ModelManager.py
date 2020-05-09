from __future__ import absolute_import, division, print_function, unicode_literals

# Install TensorFlow
import json
import os
import random

import tensorflow as tf
from tensorflow.contrib import lite


class ModelManager(object):
    usersDirectory = "UserDatas"
    train_labels = None
    test_labels = None
    train_images = None
    test_images = None

    # Define a simple sequential model
    def __init__(self):
        (self.train_images, self.train_labels), (self.test_images, self.test_labels) = tf.keras.datasets.mnist.load_data()

        self.train_labels = self.train_labels[:1000]
        self.test_labels = self.test_labels[:1000]

        self.train_images = self.train_images[:1000].reshape(-1, 28 * 28) / 255.0
        self.test_images = self.test_images[:1000].reshape(-1, 28 * 28) / 255.0

    def create_model(self, userData):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(512, activation='relu', input_shape=(784,)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(10, activation='softmax')
        ])

        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])

        return model


    def save_model(self, model, userData):
        # Save the entire model to a HDF5 file.
        # The '.h5' extension indicates that the model should be saved to HDF5.
        dir = self.usersDirectory + "/" + userData['uid']
        if not os.path.exists(dir):
            os.makedirs(dir)
        model.save(dir + '/model.h5')
        with open(dir + '/data.json', 'w+') as outfile:
            userData.update(
                {
                    'slow_insuline': [],
                    'rapid_insuline': [],
                    'hbA1cs': [],
                    'length': 0,
                    'weight': 0,
                    'sport_activities': [],
                    'meals': [],
                    'insulin': random.randint(7, 11)
                }
            )
            json.dump(userData, outfile)
            converter = lite.TFLiteConverter.from_keras_model_file(dir + '/model.h5')
            tfmodel = converter.convert()
            open(dir + "/model.tflite", "wb").write(tfmodel)
            return userData

    def train_model(self, model, userData):
        model.fit(self.train_images, self.train_labels, epochs=5)
        model.summary()

    def load_model(self, userData):
        with open(self.usersDirectory + "/" + userData['uid'] + '/data.json', 'r') as myfile:
            data = myfile.read()
        return tf.keras.models.load_model(self.usersDirectory + "/" + userData['uid'] + '/model.h5'), json.loads(data)['insulin']

    def evaluate_model(self, model, userData):
        return model.evaluate(self.test_images,  self.test_labels, verbose=2, steps=10)
