import numpy as np
from cv2 import cv2
import os

"""A module for converting an image to grayscale using numpy.

The module contains two functions: 
- grayscale_filter for converting, and saving, an image to grayscale
- numpy_color2gray for converting a ndarray representing an image to grayscale
"""

def numpy_color2gray(image_array):
    """Converts a color image array to grayscale using numpy.

    Args:
        image (ndarray): 3D array of unsigned integers representing the color image.

    Returns:
        ndarray: 2D array of unsigned integers, representing the greyscale image.
    """
    B_array = np.array(image_array[:, :, 0], dtype=float) * 0.07
    G_array = np.array(image_array[:, :, 1], dtype=float) * 0.72
    R_array = np.array(image_array[:, :, 2], dtype=float) * 0.21

    weighted_sum = B_array + G_array + R_array

    return weighted_sum.astype("uint8")


def grayscale_filter(input_filename):
    """Converts, and saves, a color image to grayscale using numpy.

    The grayscale image is written to the same directory as the original with _grayscale appended to the original name
    
    Args:
        input_filename (string): The image path.

    Returns:
        ndarray: 2D array of unsigned integers representing the greyscale image.
    """
    image_array = cv2.imread(input_filename)

    grayscale_image = numpy_color2gray(image_array)

    filename, file_extension = os.path.splitext(input_filename)
    cv2.imwrite(filename + "_grayscale" + file_extension, grayscale_image)

    return grayscale_image
