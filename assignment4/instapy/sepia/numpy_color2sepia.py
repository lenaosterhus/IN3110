import numpy as np
from cv2 import cv2
import os

def numpy_color2sepia(image_array):
    """Converts a color image array to sepia.

    Args:
        image (ndarray): 3D array of unsigned integers representing the color image.
    Returns:
        ndarray: 3D array of unsigned integers representing the sepia image.
    """
    B_array = np.array(image_array[:, :, 0], dtype=float)
    G_array = np.array(image_array[:, :, 1], dtype=float)
    R_array = np.array(image_array[:, :, 2], dtype=float)

    sepia_array_BGR = np.array([[0.131, 0.534, 0.272], [0.168, 0.686, 0.349],
                            [0.189, 0.769, 0.393]], dtype=float)

    for channel in range(3):
        B_weighted_array = B_array * sepia_array_BGR[channel, 0]
        G_weighted_array = G_array * sepia_array_BGR[channel, 1]
        R_weighted_array = R_array * sepia_array_BGR[channel, 2]

        weighted_sum = B_weighted_array + G_weighted_array + R_weighted_array
        weighted_sum = _valid_value(weighted_sum)

        image_array[:, :, channel] = weighted_sum

    return image_array.astype("uint8")

@np.vectorize
def _valid_value(num):
    # Checks if the arg is a valid value, i.e. 255 or below
    if num > 255:
        return 255
    return num


def sepia_filter(input_filename):
    """Converts a color image to sepia using Numpy.

    The sepia image is written to the same directory as the original with _sepia appended to the original name.

    Args:
        input_filename (string): the image's filepath.

    Returns:
        ndarray: 3D array of unsigned integers, representing the sepia image.
    """
    image_array = cv2.imread(input_filename)

    sepia_image = numpy_color2sepia(image_array)

    filename, file_extension = os.path.splitext(input_filename)
    cv2.imwrite(filename + "_sepia" + file_extension, sepia_image)
    return sepia_image
