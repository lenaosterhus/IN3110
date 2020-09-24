from cv2 import cv2
import numpy as np
import os

def python_color2gray(image_array):
    """Converts a color image array to grayscale.

    Args:
        image (ndarray): 3D array of unsigned integers representing the color image.
    Returns:
        ndarray: 2D array of unsigned integers representing the greyscale image.
    """
    shape = image_array.shape
    grayscale_image = np.empty((shape[0], shape[1]))

    for row_index, row in enumerate(image_array):
        for column_index, column in enumerate(row):
            B = column[0] * 0.07
            G = column[1] * 0.72
            R = column[2] * 0.21

            weighted_sum = B + G + R

            grayscale_image[row_index, column_index] = weighted_sum

    grayscale_image = grayscale_image.astype("uint8")
    return grayscale_image

def grayscale_filter(input_filename):
    """Converts a color image to grayscale.

    The grayscale image is written to the same directory as the original with _grayscale appended to the original name
    
    Args:
        input_filename (string): The image path.
    Returns:
        ndarray: 2D array of unsigned integers representing the greyscale image.
    """
    image_array = cv2.imread(input_filename)

    grayscale_image = python_color2gray(image_array)

    filename, file_extension = os.path.splitext(input_filename)
    cv2.imwrite(filename + "_grayscale" + file_extension, grayscale_image)
    
    return grayscale_image
