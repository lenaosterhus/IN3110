from cv2 import cv2
import os

from instapy.grayscale.numpy_color2gray import numpy_color2gray
from instapy.grayscale.numba_color2gray import numba_color2gray
from instapy.grayscale.python_color2gray import python_color2gray

from instapy.sepia.numpy_color2sepia import numpy_color2sepia
from instapy.sepia.numba_color2sepia import numba_color2sepia
from instapy.sepia.python_color2sepia import python_color2sepia

"""A module for adding filters to image files.

The module contains two functions: a grayscale filter and a sepia filter.
"""

def grayscale_image(input_filename, output_filename=None, implementation="numpy", scale=1.0):
    """Converts a color image to grayscale.

    Args:
        input_filename (string): the image's filepath.
        output_filename (string, optional): The filepath for where to save the result (incl. file extension). Defaults to None.
        implementation (string, optional): The implementation for the conversion. Options are "python", "numba" and "numpy". Defaults to "numpy".
        scale (float, optional): Value for how much to scale the image down. Must be > 0 and <= 1.0. Defaults to 1.0.

    Raises:
        FileNotFoundError: If the input_filename does not exist.
        ValueError: If the wrong implementation type or scale is given.

    Returns:
        ndarray: 2D array of unsigned integers, representing the grayscale image.
    """

    # Checks that the input file exists
    if not os.path.isfile(input_filename):
        raise FileNotFoundError(f"File {input_filename} does not exist")
    image_array = cv2.imread(input_filename)

    # Checks for scaling
    if scale > 1 or scale <= 0:
        raise ValueError(
            f"Scaling with {scale} is not possible. Must be > 0 and <= 1.0")
    elif scale < 1 and scale > 0:
        image_array = cv2.resize(image_array, (0, 0), fx=scale, fy=scale)

    # Uses given implementation
    if implementation == "numpy":
        grayscale_image = numpy_color2gray(image_array)
    elif implementation == "numba":
        grayscale_image = numba_color2gray(image_array)
    elif implementation == "python":
        grayscale_image = python_color2gray(image_array)
    else:
        raise ValueError(
            f"Implementation '{implementation}' is not valid. Must be 'python', 'numba' or 'numpy'")

    # Checks whether to save image or not
    if output_filename is not None:
        cv2.imwrite(output_filename, grayscale_image)

    return grayscale_image


def sepia_image(input_filename, output_filename=None, implementation="numpy", scale=1.0):
    """Converts a color image to sepia.

    Args:
        input_filename (string): the image's filepath.
        output_filename (string, optional): The filepath for where to save the result (inkl. file extension). Defaults to None.
        implementation (string, optional): The implementation for the conversion. Options are "python", "numba" and "numpy". Defaults to "numpy".
        scale (float, optional): Value for how much to scale the image down. Must be > 0 and <= 1.0. Defaults to 1.0.

    Raises:
        FileNotFoundError: If the input_filename does not exist.
        ValueError: If the wrong implementation type or scale is given.

    Returns:
        ndarray: 3D array of unsigned integers, representing the sepia image.
    """

    # Checks that the input file exists
    if not os.path.isfile(input_filename):
        raise FileNotFoundError(f"File {input_filename} does not exist")
    image_array = cv2.imread(input_filename)

    # Checks for scaling
    if scale > 1 or scale <= 0:
        raise ValueError(
            f"Scaling with {scale} is not possible. Must be > 0 and <= 1.0")
    elif scale < 1 and scale > 0:
        image_array = cv2.resize(image_array, (0, 0), fx=scale, fy=scale)

    # Uses given implementation
    if implementation == "numpy":
        sepia_image = numpy_color2sepia(image_array)
    elif implementation == "numba":
        sepia_image = numba_color2sepia(image_array)
    elif implementation == "python":
        sepia_image = python_color2sepia(image_array)
    else:
        raise ValueError(
            f"Implementation '{implementation}' is not valid. Must be 'python', 'numba' or 'numpy'")

    # Checks whether to save image or not
    if output_filename is not None:
        cv2.imwrite(output_filename, sepia_image)

    return sepia_image
