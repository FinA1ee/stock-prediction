import numpy as np
import pandas as pd
import tensorflow as tf
from keras.utils import np_utils
from tensorflow import keras
from tensorflow.keras import layers
from keras.layers import Dense, Conv1D, MaxPooling1D, Flatten, Dropout
import os
import glob

# python "E:/current term/cs 451/project/stock-prediction/scripts/pyspark_lstm_train.py"
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

path = 'E:/current term/cs 451/project/stock-prediction/data/data_processed/'
all_files = glob.glob(path + "/*.csv")
li = []
for filename in all_files:
	df = pd.read_csv(filename, index_col=None, header=0)
	li.append(df)
train = pd.concat(li, axis=0, ignore_index=True)
labels = train.values[:,-1].astype('float32')
X_train = train.values[:,-1].astype('float32')
#X_test = pd.read_csv('E:/current term/cs 451/project/stock-prediction/data/data_processed/*.csv').values[:,:-1]

# convert list of labels to binary class matrix
y_train = np_utils.to_categorical(labels)

input_dim = X_train.shape[1]
nb_classes = y_train.shape[1]
#input_dim_2 = X_test.shape[1]
X_train = X_train.reshape(-1, 1, input_dim)
print(X_train.shape)
#X_test = X_test.reshape(-1, input_dim_2, 1)

model = keras.Sequential()
model.add(layers.Embedding(input_dim = input_dim + 1, output_dim = 64))
model.add(layers.GRU(256, return_sequences=True))
model.add(layers.Conv1D(64, 1, activation='relu'))
model.add(layers.Bidirectional(layers.LSTM(256, return_sequences=True)))
model.add(layers.Bidirectional(layers.LSTM(128)))
#model.add(layers.SimpleRNN(256))
model.add(Flatten())
model.add(Dense(32, activation='relu'))
model.add(layers.Dense(nb_classes, activation='softmax'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

checkpoint_path = "stock_lstm/cp.ckpt"
#model.load_weights("stock_lstm/cp.ckpt")
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

print("Training...")
model.fit(X_train, y_train, epochs=10, batch_size=1, callbacks=[cp_callback])

print("Generating test predictions...")
preds = np.argmax(model.predict(X_train), axis=-1)

def write_preds(preds, fname):
    pd.DataFrame({"id": list(range(0,len(preds))), "label": preds}).to_csv(fname, index=False, header=True)

write_preds(preds, "E:/current term/cs 451/project/stock-prediction/data/data_prediction/predict_lstm.csv")
