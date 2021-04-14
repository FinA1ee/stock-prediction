import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.utils import np_utils
from keras.layers import Dense, Conv1D, AveragePooling1D, Flatten, Dropout
import tensorflow as tf
import os
import glob

# python "scripts/pyspark_cnn_train.py"
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

path = 'data/data_processed/'
all_files = glob.glob(path + "/*.csv")
li = []
for filename in all_files:
	df = pd.read_csv(filename, index_col=None, header=0)
	li.append(df)
train = pd.concat(li, axis=0, ignore_index=True)
labels = train.values[:,-1].astype('float32')
X_train = train.values[:,[2,3,4,5,7,8,9,17,18]].astype('float32') # change this when we add more features
#X_test = pd.read_csv('data/data_processed/*.csv').values[:,:-1]

y_train = np_utils.to_categorical(labels)

input_dim = X_train.shape[1]
nb_classes = y_train.shape[1]
#input_dim_2 = X_test.shape[1]
X_train = X_train.reshape(-1, input_dim, 1)
print(X_train.shape)
#X_test = X_test.reshape(-1, input_dim_2, 1)

model = Sequential()
model.add(Conv1D(64, 1, activation='relu', input_shape=(input_dim, 1)))
model.add(Conv1D(64, 1, activation='relu'))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(nb_classes, activation='softmax'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

checkpoint_path = "stock_cnn/cp.ckpt"
#model.load_weights("stock_cnn/cp.ckpt")
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

print("Training...")
model.fit(X_train, y_train, epochs=10, batch_size=1, callbacks=[cp_callback])

print("Generating test predictions...")
preds = np.argmax(model.predict(X_train), axis=-1)

def write_preds(preds, fname):
    pd.DataFrame({"id": list(range(0,len(preds))), "label": preds}).to_csv(fname, index=False, header=True)

write_preds(preds, "data/data_prediction/predict_cnn.csv")
