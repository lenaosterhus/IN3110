from instapy.sepia import python_color2sepia as py
from instapy.sepia import numpy_color2sepia as np
from instapy.sepia import numba_color2sepia as nb
import time
from cv2 import cv2



image_array = cv2.imread("rain.jpg")

# Python
my_times_python = []
for i in range(3):
    tic = time.perf_counter()
    py.python_color2sepia(image_array)
    toc = time.perf_counter()
    duration = toc - tic
    my_times_python.append(duration)

avg_time_python = sum(my_times_python)/len(my_times_python)

with open("./reports/python_report_color2sepia.txt", "w") as file:
    file.write(f"""Timing: python_color2sepia
Dimensions: 400, 600, 3
Average runtime running python_color2sepia after 3 runs: {avg_time_python:.2f} s
Timing performed using: time.perf_counter()""")

# Numpy
my_times_numpy = []
for i in range(3):
    tic = time.perf_counter()
    np.numpy_color2sepia(image_array)
    toc = time.perf_counter()
    duration = toc - tic
    my_times_numpy.append(duration)

avg_time_numpy = sum(my_times_numpy)/len(my_times_numpy)

with open("./reports/numpy_report_color2sepia.txt", "w") as file:
    file.write(f"""Timing: numpy_color2sepia
Dimensions: 400, 600, 3
Average runtime running numpy_color2sepia after 3 runs: {avg_time_numpy:.4f} s
Average runtime running of numpy_color2sepia is {(avg_time_python/avg_time_numpy):.0f} times faster than python_color2sepia
Timing performed using: time.perf_counter()""")

# Numba
my_times_numba = []
for i in range(3):
    tic = time.perf_counter()
    nb.numba_color2sepia(image_array)
    toc = time.perf_counter()
    duration = toc - tic
    my_times_numba.append(duration)

avg_time_numba = sum(my_times_numba)/len(my_times_numba)

with open("./reports/numba_report_color2sepia.txt", "w") as file:
    file.write(f"""Timing: numba_color2sepia
Dimensions: 400, 600, 3
Average runtime running numba_color2sepia after 3 runs: {avg_time_numba:.2f} s
Average runtime for running numba_color2sepia is {(avg_time_python/avg_time_numba):.0f} times faster than python_color2sepia
Average runtime for running numba_color2sepia is {(avg_time_numpy/avg_time_numba):.2f} times faster than numpy_color2sepia
Timing performed using: time.perf_counter()""")
