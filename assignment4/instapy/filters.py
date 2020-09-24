from cv2 import cv2
import numpy as np
from instapy.grayscale.numpy_color2gray import numpy_color2gray
from instapy.sepia.numpy_color2sepia import numpy_color2sepia

def grayscale_image(input_filename, output_filename=None):
    """Converts a color image to grayscale.

    Args:
        input_filename (string): the image's filepath.
        output_filename (string, optional): The filepath for where to save the result (inkl. file extension). Defaults to None.

    Returns:
        ndarray: 2D array of unsigned integers, representing the grayscale image.
    """
    image_array = cv2.imread(input_filename)

    grayscale_image = numpy_color2gray(image_array)

    if output_filename != None:
        cv2.imwrite(output_filename, grayscale_image)
    return grayscale_image
    
    
def sepia_image(input_filename, output_filename=None):
    """Converts a color image to sepia.

    Args:
        input_filename (string): the image's filepath.
        output_filename (string, optional): The filepath for where to save the result (inkl. file extension). Defaults to None.

    Returns:
        ndarray: 3D array of unsigned integers, representing the sepia image.
    """
    image_array = cv2.imread(input_filename)

    sepia_image = numpy_color2sepia(image_array)

    if output_filename != None:
        cv2.imwrite(output_filename, sepia_image)
    return sepia_image
