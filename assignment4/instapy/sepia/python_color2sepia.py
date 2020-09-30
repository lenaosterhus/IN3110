from cv2 import cv2
import numpy as np
import os

"""A module for converting an image to sepia using only python.

The module contains two functions: 
- sepia_filter for converting, and saving, an image to sepia
- python_color2sepia for converting a ndarray representing an image to sepia
"""

def python_color2sepia(image_array):
    """Converts a color image array to sepia.

    Args:
        image (ndarray): 3D array of unsigned integers representing the color image.
    Returns:
        ndarray: 3D array of unsigned integers representing the sepia image.
    """
    sepia_array = np.array(image_array)

    for row_index, row in enumerate(image_array):
        for column_index, column in enumerate(row):

            for channel in range(3):
                if channel == 0:
                    # Blue
                    B_weight = 0.131
                    G_weight = 0.534
                    R_weight = 0.272

                elif channel == 1:
                    # Green
                    B_weight = 0.168
                    G_weight = 0.686
                    R_weight = 0.349

                elif channel == 2:
                    # Red
                    B_weight = 0.189
                    G_weight = 0.769
                    R_weight = 0.393

                B = column[0] * B_weight
                G = column[1] * G_weight
                R = column[2] * R_weight

                weighted_sum = B + G + R

                sepia_array[row_index, column_index, channel] = weighted_sum if weighted_sum < 255 else 255
    
    return sepia_array.astype("uint8")


def sepia_filter(input_filename):
    """Converts, and saves, a color image to sepia.

    The sepia image is written to the same directory as the original with _sepia appended to the original name.

    Args:
        input_filename (string): the image's filepath.

    Returns:
        ndarray: 3D array of unsigned integers, representing the sepia image.
    """
    image_array = cv2.imread(input_filename)

    sepia_image = python_color2sepia(image_array)

    filename, file_extension = os.path.splitext(input_filename)
    cv2.imwrite(filename + "_sepia" + file_extension, sepia_image)
    return sepia_image
