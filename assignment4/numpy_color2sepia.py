from cv2 import cv2
import numpy as np
import os
import time


def numpy_color2sepia(image):
    """Converts a image from color to sepia.

    The sepia image is written to the same directory as the original with _sepia appended to the original name

    Args:
        image (string): The image path
    """
    image_array = cv2.imread(image)

    filename, file_extension = os.path.splitext(image)

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

    sepia_image = image_array.astype("uint8")
    cv2.imwrite(filename + "_sepia" + file_extension, sepia_image)

@np.vectorize
def _valid_value(num):
    # Checks if the arg is a valid value, i.e. 255 or below
    if num > 255:
        return 255
    return num

# If run as a script: Time 3 runs and log to file
if __name__ == "__main__":
    my_times = []
    for i in range(3):
        tic = time.perf_counter()
        numpy_color2sepia("rain.jpg")
        toc = time.perf_counter()
        duration = toc - tic
        my_times.append(duration)

    avg_time = sum(my_times)/len(my_times)

    with open("numpy_report_color2sepia.txt", "w") as file:
        file.write(f"""Timing: numpy_color2sepia
Dimensions: 400, 600, 3
Average runtime running numpy_color2sepia after 3 runs: {avg_time:.2f} s
Average runtime for running numpy_color2sepia is {(8.06/avg_time):.0f} times faster than python_color2sepia
Timing performed using: time.perf_counter()""")
