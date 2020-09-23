from cv2 import cv2
import numpy as np
import os
import time


def numpy_color2gray(image):
    """Converts a color image to grayscale.

    The grayscale image is written to the same directory as the original with _grayscale appended to the original name

    Args:
        image (string): The image path
    """
    image_array = cv2.imread(image)
    filename, file_extension = os.path.splitext(image)

    B_array = np.array(image_array[:,:,0], dtype=float)
    G_array = np.array(image_array[:,:,1], dtype=float)
    R_array = np.array(image_array[:,:,2], dtype=float)

    B_array *= 0.07
    G_array *= 0.72
    R_array *= 0.21

    weighted_sum = B_array + G_array + R_array

    grayscale_image = weighted_sum.astype("uint8")
    cv2.imwrite(filename + "_grayscale" + file_extension, grayscale_image)


# If run as a script: Time 3 runs and log to file
if __name__ == "__main__":
    my_times = []
    for i in range(3):
        tic = time.perf_counter()
        numpy_color2gray("rain.jpg")
        toc = time.perf_counter()
        duration = toc - tic
        my_times.append(duration)

    avg_time = sum(my_times)/len(my_times)

    with open("numpy_report_color2gray.txt", "w") as file:
        file.write(f"""Timing: numpy_color2gray
Dimensions: 400, 600, 3
Average runtime running numpy_color2gray after 3 runs: {avg_time:.4f} s
Average runtime running of numpy_color2gray is {(2.51/avg_time):.0f} times faster than python_color2gray
Timing performed using: time.perf_counter()""")
