from cv2 import cv2
import numpy as np
import os
import time

def python_color2gray(image):
    """Converts a color image to grayscale.

    The grayscale image is written to the same directory as the original with _grayscale appended to the original name

    Args:
        image (string): The image path
    """
    image_array = cv2.imread(image)
    shape = image_array.shape
    filename, file_extension = os.path.splitext(image)
    grayscale_image = np.empty((shape[0], shape[1]))

    for row_index, row in enumerate(image_array):
        for column_index, column in enumerate(row):
            B = column[0] * 0.07
            G = column[1] * 0.72
            R = column[2] * 0.21

            weighted_sum = B + G + R

            grayscale_image[row_index, column_index] = weighted_sum

    grayscale_image = grayscale_image.astype("uint8")
    cv2.imwrite(filename + "_grayscale" + file_extension, grayscale_image)


# If run as a script: Time 3 runs and log to file
if __name__ == "__main__":
    my_times = []
    for i in range(3):
        tic = time.perf_counter()
        python_color2gray("rain.jpg")
        toc = time.perf_counter()
        duration = toc - tic
        my_times.append(duration)

    avg_time = sum(my_times)/len(my_times)

    with open("python_report_color2gray.txt", "w") as file:
        file.write(f"""Timing: python_color2gray
Dimensions: 400, 600, 3
Average runtime running python_color2gray after 3 runs: {avg_time:.2f} s
Timing performed using: time.perf_counter()""")

