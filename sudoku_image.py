from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import numpy as np
import imutils
import cv2


def find_sudoku_grid(image):
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(grayscale_image, (7, 7), 3)
    thresh = cv2.adaptiveThreshold(blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    thresh = cv2.bitwise_not(thresh)

    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    grid_contours = None

    for c in contours:
        # approximate the contour
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
        if len(approx) == 4:
            grid_contours = approx
            break

    if grid_contours is None:
        raise Exception("Could not find Sudoku puzzle grid.")

    top_down_grid = four_point_transform(image, grid_contours.reshape(4, 2))
    warped_grid = four_point_transform(grayscale_image, grid_contours.reshape(4, 2))

    return top_down_grid, warped_grid


def detect_digits(cell):
    thresh = cv2.threshold(cell, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    thresh = clear_border(thresh)

    digit_contour = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    digit_contour = imutils.grab_contours(digit_contour)

    # empty cell
    if len(digit_contour) == 0:
        return None

    cnt = max(digit_contour, key=cv2.contourArea)
    mask = np.zeros(thresh.shape, dtype="uint8")
    cv2.drawContours(mask, [cnt], -1, 255, -1)

    h, w = thresh.shape
    filled_percent = cv2.countNonZero(mask) / float(w * h)

    if filled_percent < 0.025:
        return None

    digit = cv2.bitwise_and(thresh, thresh, mask=mask)

    return digit
