from cv2 import cv2
import os
import time
from numba import jit


def numba_color2grey(image):
    image_array = cv2.imread(image)
    filename, file_extension = os.path.splitext(image)

    greyscale_image = _conversion(image_array).astype("uint8")
    cv2.imwrite(filename + "_greyscale" + file_extension, greyscale_image)

@jit
def _conversion(image_array):
    for row in image_array:
        for column in row:
            B = column[0] * 0.07
            G = column[1] * 0.72
            R = column[2] * 0.21

            weighted_sum = B + G + R

            column[0] = column[1] = column[2] = weighted_sum

    return image_array

if __name__ == "__main__":
    my_times = []
    for i in range(3):
        tic = time.perf_counter()
        numba_color2grey("rain.jpg")
        toc = time.perf_counter()
        duration = toc - tic
        my_times.append(duration)

    avg_time = sum(my_times)/len(my_times)

    with open("numba_report_color2grey.txt", "w") as file:
        file.write(f"""Timing: numba_color2grey
Dimensions: 400, 600, 3
Average runtime running numba_color2grey after 3 runs: {avg_time:.2f} s
Average runtime for running numba_color2grey is {(2.78/avg_time):.0f} times faster than python_color2grey
Average runtime for running numba_color2grey is {(avg_time/0.02):.0f} times slower than numpy_color2grey
Timing performed using: time.perf_counter()""")
