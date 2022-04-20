# === CELL ===
#Importing Libraries
from keras.layers import Input,Dense,Flatten
from keras.models import Model
from tensorflow.keras import layers
from keras.applications.xception import Xception
from keras.applications.xception import preprocess_input
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
import numpy as np
from glob import glob

import tensorflow as tf
import tf.data


# === CELL ===
# re-size all the images to this
IMAGE_SIZE = [224, 224]

DS_DIR = 'ds0'
train_path = f'{DS_DIR}/train'
valid_path = f'{DS_DIR}/valid'
test_path = f'{DS_DIR}/test'


# === CELL ===
xcept = Xception(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

# don't train existing weights
for layer in xcept.layers:
  layer.trainable = False

#Getting Number of Categories
folders = glob(f'{train_path}/*')
x = Flatten()(xcept.output)
x = layers.Dense(256, 'relu', kernel_initializer='he_normal')(x)
x = layers.BatchNormalization()(x)
x = layers.Dropout(0.3)(x)


# === CELL ===
prediction = Dense(len(folders), activation='softmax')(x)

# create a model object
model = Model(inputs=xcept.input, outputs=prediction)
print(model.summary())


# === CELL ===
# tell the model what cost and optimization method to use
model.compile(
  loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)



# === CELL ===
#Data Augmentation
from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

valid_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory(train_path,
  target_size = (224, 224), batch_size = 64, class_mode = 'categorical')
valid_set = valid_datagen.flow_from_directory(valid_path,
  target_size = (224, 224), batch_size = 64, class_mode = 'categorical')

test_set = test_datagen.flow_from_directory(test_path,
  target_size = (224, 224), batch_size = 64, class_mode = 'categorical')


# === CELL ===
#Fitting the model
r = model.fit(
  training_set,
  validation_data=valid_set,
  epochs=10,
  steps_per_epoch=len(training_set),
  validation_steps=len(valid_set),
  use_multiprocessing=True,
  workers=10,
)


# === CELL ===
#Saving the Model.
import tensorflow as tf

from keras.models import load_model
model.save('./bird_classification_new_model.h5')
