from instapy.grayscale import python_color2gray, numpy_color2gray, numba_color2gray

from instapy.sepia import python_color2sepia, numpy_color2sepia, numba_color2sepia

from instapy import filters
from cv2 import cv2
import numpy as np
import pytest

@pytest.fixture
def img_array():
    # Create an image with random pixel values to be used for testing
    shape = (10, 10, 3)
    img_array = np.random.randint(0, 256, shape)
    cv2.imwrite("test_img_array.jpg", img_array)
    return img_array

def test_grayscale(img_array):
    shape = (10, 10, 3)
    test_img_name = "test_img_array.jpg"
    original_img = cv2.imread(test_img_name)
    

    ## Test filters.grayscale_image()
    grayscale_img = filters.grayscale_image(test_img_name)

    # Test shape
    assert grayscale_img.shape == (shape[0], shape[1])
    
    # Test a selected pixel
    original_pixel = original_img[0, 0]
    grayscale_pixel = grayscale_img[0, 0]

    expected_value = int((original_pixel[0] * 0.07 + 
                      original_pixel[1] * 0.72 + 
                      original_pixel[2] * 0.21).item())

    assert grayscale_pixel == expected_value


    ## Test all implementations of grayscale_filter
    grayscale_img_python = python_color2gray.grayscale_filter(test_img_name)
    grayscale_img_numpy = numpy_color2gray.grayscale_filter(test_img_name)
    grayscale_img_numba = numba_color2gray.grayscale_filter(test_img_name)

    # Test shape
    assert grayscale_img_python.shape == (shape[0], shape[1])
    assert grayscale_img_numpy.shape == (shape[0], shape[1])
    assert grayscale_img_numba.shape == (shape[0], shape[1])

    # Test a selected pixel
    grayscale_pixel_python = grayscale_img_python[0, 0]
    grayscale_pixel_numpy = grayscale_img_numpy[0, 0]
    grayscale_pixel_numba = grayscale_img_numba[0, 0]

    assert grayscale_pixel_python == expected_value
    assert grayscale_pixel_numpy == expected_value
    assert grayscale_pixel_numba == expected_value


def test_sepia(img_array):
    shape = (10, 10, 3)
    test_img_name = "test_img_array.jpg"
    original_img = cv2.imread(test_img_name)


    ## Test filters.sepia_image()
    sepia_img = filters.sepia_image(test_img_name)

    # Test shape
    assert sepia_img.shape == original_img.shape

    # Test a selected pixel
    original_pixel = original_img[0, 0]

    expected_value_channel0 = (original_pixel[0] * 0.131 +
                               original_pixel[1] * 0.534 +
                               original_pixel[2] * 0.272).item()
    expected_value_channel1 = (original_pixel[0] * 0.168 +
                               original_pixel[1] * 0.686 +
                               original_pixel[2] * 0.349).item()
    expected_value_channel2 = (original_pixel[0] * 0.189 +
                               original_pixel[1] * 0.769 +
                               original_pixel[2] * 0.393).item()

    # Correct for overflow
    expected_value_channel0 = expected_value_channel0 if expected_value_channel0 < 255 else 255
    expected_value_channel1 = expected_value_channel1 if expected_value_channel1 < 255 else 255
    expected_value_channel2 = expected_value_channel2 if expected_value_channel2 < 255 else 255
    
    expected_values = np.array([
        expected_value_channel0, 
        expected_value_channel1, 
        expected_value_channel2], dtype="uint8")

    assert np.array_equal(sepia_img[0, 0], expected_values)


    ## Test all the sepia_filter implementations
    sepia_img_python = python_color2sepia.sepia_filter(test_img_name)
    sepia_img_numpy = numpy_color2sepia.sepia_filter(test_img_name)
    sepia_img_numba = numba_color2sepia.sepia_filter(test_img_name)

    # Test shape
    assert sepia_img_python.shape == original_img.shape
    assert sepia_img_numpy.shape == original_img.shape
    assert sepia_img_numba.shape == original_img.shape

    # Test a selected pixel
    assert np.array_equal(sepia_img_python[0, 0], expected_values)
    assert np.array_equal(sepia_img_numpy[0, 0], expected_values)
    assert np.array_equal(sepia_img_numba[0, 0], expected_values)

