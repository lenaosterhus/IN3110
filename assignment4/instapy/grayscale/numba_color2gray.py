from numba import jit
import numpy as np
from cv2 import cv2
import os

"""A module for converting an image to grayscale using numba.

The module contains two functions: 
- grayscale_filter for converting, and saving, an image to grayscale
- numba_color2gray for converting a ndarray representing an image to grayscale
"""


def numba_color2gray(image_array):
    """Converts a color image array to grayscale using numba.

    Args:
        image (ndarray): 3D array of unsigned integers representing the color image.
        
    Returns:
        ndarray: 2D array of unsigned integers, representing the greyscale image.
    """
    return _conversion(image_array).astype("uint8")


@jit
def _conversion(image_array):
    # Converts the values in the image channels to grayscale values
    shape = image_array.shape
    grayscale_image = np.empty((shape[0], shape[1]))

    for row_index, row in enumerate(image_array):
        for column_index, column in enumerate(row):
            B = column[0] * 0.07
            G = column[1] * 0.72
            R = column[2] * 0.21

            weighted_sum = B + G + R

            grayscale_image[row_index, column_index] = weighted_sum

    return grayscale_image


def grayscale_filter(input_filename):
    """Converts, and saves, a color image to grayscale using Numba.

    The grayscale image is written to the same directory as the original with _grayscale appended to the original name
    
    Args:
        input_filename (string): The image path.

    Returns:
        ndarray: 2D array of unsigned integers representing the greyscale image.
    """
    image_array = cv2.imread(input_filename)

    grayscale_image = numba_color2gray(image_array)

    filename, file_extension = os.path.splitext(input_filename)
    cv2.imwrite(filename + "_grayscale" + file_extension, grayscale_image)

    return grayscale_image
