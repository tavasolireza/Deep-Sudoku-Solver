import sudoku_CNN as scnn
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.datasets import mnist
from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import classification_report

((train_data, train_label), (test_data, test_label)) = mnist.load_data()

train_data = train_data.reshape((train_data.shape[0], train_data.shape[1], train_data.shape[2], 1))
test_data = test_data.reshape((test_data.shape[0], test_data.shape[1], test_data.shape[2], 1))

train_data = train_data.astype("float32") / 255.0
test_data = test_data.astype("float32") / 255.0

train_label = to_categorical(train_label, 10)
test_label = to_categorical(test_label, 10)

