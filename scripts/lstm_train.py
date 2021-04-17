import numpy as np
import pandas as pd
import tensorflow as tf
from keras.utils import np_utils
from tensorflow import keras
from tensorflow.keras import layers
from keras.layers import Dense, Conv1D, Flatten
from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
import glob

# python "scripts/pyspark_lstm_train.py"
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

path = 'data/data_processed/'
all_files = glob.glob(path + "/*.csv")
li = []
for filename in all_files:
	df = pd.read_csv(filename, index_col=None, header=0)
	li.append(df)
all = pd.concat(li, axis=0, ignore_index=True)

train = None
test = None
split_randomly = True
if split_randomly:
    train = all.sample(frac = 0.7, random_state = 200)
    test = all.drop(train.index)
else:
    train = all.iloc[:5000,:]
    test = all.iloc[5001:,:]

labels = train.values[:,-1]
X_train = train.values[:,16]
vocab_size = 5000
encoded_docs = [one_hot(d, vocab_size) for d in X_train]
max_length = 100
padded_docs = pad_sequences(encoded_docs, maxlen=max_length, padding='post')
y_train = np_utils.to_categorical(labels)
nb_classes = y_train.shape[1]

X_test = test.values[:,16]
labels2 = test.values[:,-1]
encoded_docs2 = [one_hot(d, vocab_size) for d in X_test]
padded_docs2 = pad_sequences(encoded_docs2, maxlen=max_length, padding='post')
y_test = np_utils.to_categorical(labels2)

model = keras.Sequential()
model.add(layers.Embedding(vocab_size, 64, input_length=max_length))
model.add(layers.GRU(256, return_sequences=True))
model.add(layers.Conv1D(64, 1, activation='relu'))
model.add(layers.Bidirectional(layers.LSTM(256, return_sequences=True)))
model.add(layers.Bidirectional(layers.LSTM(128)))
model.add(Flatten())
model.add(Dense(32, activation='relu'))
model.add(layers.Dense(nb_classes, activation='softmax'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

checkpoint_path = "stock_lstm/cp.ckpt"
# load weight after at least one epoch is trained to restore the trained model
# model.load_weights("stock_lstm/cp.ckpt")
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

print("Training...")
model.fit(padded_docs, y_train, epochs=5, batch_size=128, callbacks=[cp_callback])

print("Evaluating...")
loss, accuracy = model.evaluate(padded_docs2, y_test)
print('Accuracy: %f' % (accuracy * 100))

print("Generating test predictions...")
preds = np.argmax(model.predict(padded_docs2), axis=-1)

def write_preds(preds, fname):
    pd.DataFrame({"id": list(range(0,len(preds))), "label": preds}).to_csv(fname, index=False, header=True)

write_preds(preds, "data/data_prediction/predict_lstm.csv")

