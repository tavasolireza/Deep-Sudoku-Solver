from sudoku_image import *
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
from solve_sudoku_text import *
import imutils
import cv2

image_path = input("Enter the image's path: ")

model = load_model('digit_recognition_model.h5')

image = cv2.imread(image_path)
image = imutils.resize(image, width=600)

top_down_grid, warped_grid = find_sudoku_grid(image)

# board = np.full((1, 81), 0)
board = np.zeros((9, 9), dtype="int")
step_x = warped_grid.shape[1] // 9
step_y = warped_grid.shape[0] // 9

cell_location = []

for y in range(0, 9):
    row = []
    for x in range(0, 9):
        start_x = x * step_x
        start_y = y * step_y
        end_x = (x + 1) * step_x
        end_y = (y + 1) * step_y
        row.append((start_x, start_y, end_x, end_y))

        cell = warped_grid[start_y:end_y, start_x:end_x]
        digit = detect_digits(cell)

        if digit is not None:
            digit_input = cv2.resize(digit, (28, 28))
            digit_input = digit_input.astype("float") / 255.0
            digit_input = img_to_array(digit_input)
            digit_input = np.expand_dims(digit_input, axis=0)

            pred = model.predict(digit_input).argmax(axis=1)[0]
            board[y, x] = pred

    cell_location.append(row)

board = [str(x) if x != 0 else '.' for x in board.reshape(1, 81).tolist()[0]]
string_board = "".join(board)
display(search(grid_values(string_board)))
