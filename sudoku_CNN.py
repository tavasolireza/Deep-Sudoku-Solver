from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Dropout, Dense, MaxPooling2D, Activation, Flatten


def create_model(height, width, channel, classes):
    model = Sequential()
    shape = (height, width, channel)

    model.add(Conv2D(32, (5, 5), padding='same', input_shape=shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D((2, 2)))

    model.add(Conv2D(32, (3, 3), padding="same"))
    model.add(Activation("relu"))
    model.add(MaxPooling2D((2, 2)))

    model.add(Flatten())

    model.add(Dense(64))
    model.add(Activation("relu"))
    model.add(Dropout(0.5))

    model.add(Dense(64))
    model.add(Activation("relu"))
    model.add(Dropout(0.5))

    model.add(Dense(classes))
    model.add(Activation("softmax"))

    return model
