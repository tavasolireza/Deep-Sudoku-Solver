import sudoku_CNN as sCNN
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import classification_report

((train_data, train_label), (test_data, test_label)) = mnist.load_data()

train_data = train_data.reshape((train_data.shape[0], train_data.shape[1], train_data.shape[2], 1))
test_data = test_data.reshape((test_data.shape[0], test_data.shape[1], test_data.shape[2], 1))

train_data = train_data.astype("float32") / 255.0
test_data = test_data.astype("float32") / 255.0

train_label = to_categorical(train_label, 10)
test_label = to_categorical(test_label, 10)

model = sCNN.create_model(height=28, width=28, channel=1, classes=10)
model.compile(loss="categorical_crossentropy", optimizer=Adam(learning_rate=1e-3), metrics=["accuracy"])
model.fit(train_data, train_label, validation_data=(test_data, test_label), batch_size=128, epochs=15, verbose=1)

predictions = model.predict(test_data)

print(classification_report(test_label.argmax(axis=1), predictions.argmax(axis=1),
                            target_names=[str(x) for x in range(0, 10)]))

model.save('digit_recognition_model.h5')
