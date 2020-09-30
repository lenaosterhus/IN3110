from instapy import filters

from cv2 import cv2
import numpy as np
import pytest
import os
import importlib


@pytest.fixture(scope="session")
def original_array():
    # Create an image with random pixel values to be used for testing session

    shape = (10, 10, 3)
    test_img_name = "test_img_array.jpg"
    img_array = np.random.randint(0, 256, shape)
    cv2.imwrite(test_img_name, img_array)
    return cv2.imread(test_img_name)


class TestGrayscale:

    test_img_name = "test_img_array.jpg"

    @pytest.fixture(scope="session")
    def expected_grayscale_value(self, original_array):
        # Calculate and return the expected value for pixel (0,0) used for testing session

        original_pixel = original_array[0, 0]

        expected_value = int((original_pixel[0] * 0.07 +
                              original_pixel[1] * 0.72 +
                              original_pixel[2] * 0.21).item())
        return expected_value

    def test_filters_grayscale_image(self, original_array, expected_grayscale_value):
        # Test the filters-module in instapy-package

        grayscale_img = filters.grayscale_image(self.test_img_name)

        original_shape = original_array.shape
        expected_shape = (original_shape[0], original_shape[1])

        # Test that shape is 2D array with same width and height as original
        assert grayscale_img.shape == expected_shape

        # Test that a selected pixel has the expected value
        assert grayscale_img[0, 0] == expected_grayscale_value

    @pytest.mark.parametrize("implementation", ("python", "numpy", "numba"))
    def test_grayscale_filter(self, original_array, expected_grayscale_value, implementation):
        # Test all grayscale_filter implementations in the instapy.grayscale-package

        # Get the specific implementation being tested
        module = importlib.import_module(f"instapy.grayscale.{implementation}_color2gray")
        grayscale_filter = getattr(module, "grayscale_filter")

        grayscale_img = grayscale_filter(self.test_img_name)

        original_shape = original_array.shape
        expected_shape = (original_shape[0], original_shape[1])

        # Test that shape is 2D array with same width and height as original
        assert grayscale_img.shape == expected_shape

        # Test that a selected pixel has the expected value
        grayscale_pixel = grayscale_img[0, 0]

        assert grayscale_pixel == expected_grayscale_value


class TestSepia:

    test_img_name = "test_img_array.jpg"

    @pytest.fixture(scope="session")
    def expected_sepia_array(self, original_array):
        # Calculate and return the expected values for pixel (0,0) used for testing session

        original_pixel = original_array[0, 0]

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

        return expected_values

    def test_filters_sepia_image(self, original_array, expected_sepia_array):
        # Test the filters-module in instapy-package

        sepia_img = filters.sepia_image(self.test_img_name)

        # Test that shape is 3D array with same width and height as original
        assert sepia_img.shape == original_array.shape

        # Test that a selected pixel has the expected value
        assert np.array_equal(sepia_img[0, 0], expected_sepia_array)

    @pytest.mark.parametrize("implementation", ("python", "numpy", "numba"))
    def test_sepia_filter(self, original_array, expected_sepia_array, implementation):
        # Test all sepia_filter implementations in the instapy.sepia-package

        # Get the specific implementation being tested
        module = importlib.import_module(f"instapy.sepia.{implementation}_color2sepia")
        sepia_filter = getattr(module, "sepia_filter")

        sepia_img = sepia_filter(self.test_img_name)

        # Test that shape is 3D array with same width and height as original
        assert sepia_img.shape == original_array.shape

        # Test that a selected pixel has the expected value
        assert np.array_equal(sepia_img[0, 0], expected_sepia_array)