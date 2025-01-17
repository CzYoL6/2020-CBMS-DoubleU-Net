
import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.callbacks import *
from tensorflow.keras.optimizers import Adam, Nadam
from tensorflow.keras.metrics import *
from glob import glob
from sklearn.model_selection import train_test_split
import model2
from utils import *
from metrics import *
from tensorflow import keras

def read_image(x):
    x = x.decode()
    image = cv2.imread(x, cv2.IMREAD_COLOR)
    image = np.clip(image - np.median(image)+127, 0, 255)
    image = image/255.0
    image = image.astype(np.float32)
    return image

def read_mask(y):
    y = y.decode()
    mask = cv2.imread(y, cv2.IMREAD_GRAYSCALE)
    mask = mask/255.0
    mask = mask.astype(np.float32)
    mask = np.expand_dims(mask, axis=-1)
    return mask

def parse_data(x, y):
    def _parse(x, y):
        x = read_image(x)
        y = read_mask(y)
        y = np.concatenate([y, y], axis=-1)
        return x, y

    x, y = tf.numpy_function(_parse, [x, y], [tf.float32, tf.float32])
    x.set_shape([192, 256, 3])
    y.set_shape([192, 256, 2])
    return x, y

def tf_dataset(x, y, batch=8):
    dataset = tf.data.Dataset.from_tensor_slices((x, y))
    dataset = dataset.shuffle(buffer_size=32)
    dataset = dataset.map(map_func=parse_data, num_parallel_calls=batch)
    dataset = dataset.repeat()
    dataset = dataset.batch(batch)
    return dataset

if __name__ == "__main__":
    # Set memory growth for all GPUs
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            print("Memory growth enabled for all GPUs")
        except RuntimeError as e:
            print(e)
   
    keras.config.disable_traceback_filtering()
    
    np.random.seed(42)
    tf.random.set_seed(42)
    create_dir("files")

    train_path = "./data/"
    valid_path = "./data/"

    ## Training
    train_x = sorted(glob(os.path.join(train_path, "ISIC2018_Task1-2_Training_Input_", "*.jpg")))
    train_y = sorted(glob(os.path.join(train_path, "ISIC2018_Task1_Training_GroundTruth_", "*.png")))

    ## Shuffling
    train_x, train_y = shuffling(train_x, train_y)

    ## Validation
    valid_x = sorted(glob(os.path.join(valid_path, "ISIC2018_Task1-2_Validation_Input_", "*.jpg")))
    valid_y = sorted(glob(os.path.join(valid_path, "ISIC2018_Task1_Validation_GroundTruth_", "*.png")))

    model_path = "files/ISIC2018_my_model.keras"
    batch_size = 16
    epochs = 300
    lr = 1e-4
    shape = (192, 256, 3)

    model = model2.build_model(shape)
    metrics = [
        dice_coef,
        iou,
        Recall(),
        Precision()
    ]
    
    train_dataset = tf_dataset(train_x, train_y, batch=batch_size)
    valid_dataset = tf_dataset(valid_x, valid_y, batch=batch_size)
    
    model.compile(loss=dice_loss, optimizer=Adam(lr), metrics=metrics)

    callbacks = [
        ModelCheckpoint(model_path),
        ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=20),
        CSVLogger("files/data_my_model.csv"),
        TensorBoard(),
        EarlyStopping(monitor='val_loss', patience=50, restore_best_weights=False)
    ]

    train_steps = (len(train_x)//batch_size)
    valid_steps = (len(valid_x)//batch_size)

    if len(train_x) % batch_size != 0:
        train_steps += 1

    if len(valid_x) % batch_size != 0:
        valid_steps += 1

    model.fit(train_dataset,
            epochs=epochs,
            validation_data=valid_dataset,
            steps_per_epoch=train_steps,
            validation_steps=valid_steps,
            callbacks=callbacks,
            shuffle=False)
 