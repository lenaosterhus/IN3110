from cv2 import cv2
import os
import time


def python_color2sepia(image):
    image_array = cv2.imread(image)
    filename, file_extension = os.path.splitext(image)

    for row in image_array:
        for column in row:

            for i in range(3):
                column = _conversion(column, i)

    sepia_image = image_array.astype("uint8")
    cv2.imwrite(filename + "_sepia" + file_extension, sepia_image)


def _conversion(column, channel):
    
    if channel == 0:
        # Blue
        B_weight = 0.131
        G_weight = 0.534
        R_weight = 0.272
    
    elif channel == 1:
        # Green
        B_weight = 0.168
        G_weight = 0.686
        R_weight = 0.349

    elif channel == 2:
        # Red
        B_weight = 0.189
        G_weight = 0.769
        R_weight = 0.393

    B = column[0] * B_weight
    G = column[1] * G_weight
    R = column[2] * R_weight
    
    weighted_sum = B + G + R

    column[channel] = weighted_sum if weighted_sum < 255 else 255
    return column


if __name__ == "__main__":
    my_times = []
    for i in range(3):
        tic = time.perf_counter()
        python_color2sepia("rain.jpg")
        toc = time.perf_counter()
        duration = toc - tic
        my_times.append(duration)

    avg_time = sum(my_times)/len(my_times)

    with open("python_report_color2sepia.txt", "w") as file:
        file.write(f"""Timing: python_color2sepia
Dimensions: 400, 600, 3
Average runtime running python_color2sepia after 3 runs: {avg_time:.2f} s
Timing performed using: time.perf_counter()""")
