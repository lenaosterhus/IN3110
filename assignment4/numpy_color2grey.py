from cv2 import cv2
import numpy as np
import os
import time


def numpy_color2grey(image):
    image_array = cv2.imread(image)
    filename, file_extension = os.path.splitext(image)

    B_array = np.array(image_array[:,:,0], dtype=float)
    G_array = np.array(image_array[:,:,1], dtype=float)
    R_array = np.array(image_array[:,:,2], dtype=float)

    B_array *= 0.07
    G_array *= 0.72
    R_array *= 0.21

    weighted_sum = B_array + G_array + R_array

    image_array[:, :, 0] = image_array[:, :, 1] = image_array[:, :, 2] = weighted_sum

    greyscale_image = image_array.astype("uint8")
    cv2.imwrite(filename + "_greyscale" + file_extension, greyscale_image)


my_times = []
for i in range(3):
    tic = time.perf_counter()
    numpy_color2grey("rain.jpg")
    toc = time.perf_counter()
    duration = toc - tic
    my_times.append(duration)

avg_time = sum(my_times)/len(my_times)

with open("numpy_report_color2grey.txt", "w") as file:
    file.write(f"""Timing: numpy_color2grey
Dimensions: 400, 600, 3
Average runtime running numpy_color2grey after 3 runs: {avg_time:.2f} s
Average runtime running of numpy_color2grey is {(2.78/avg_time):.0f} times faster than python_color2grey
Timing performed using: time.perf_counter()""")
