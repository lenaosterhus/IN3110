from cv2 import cv2
import os
import time

def python_color2grey(image):
    """Converts a color image to greyscale.

    The greyscale image is written to the same directory as the original with _greyscale appended to the original name

    Args:
        image (string): The image path
    """
    image_array = cv2.imread(image)
    filename, file_extension = os.path.splitext(image)

    for row in image_array:
        for column in row:
            B = column[0] * 0.07
            G = column[1] * 0.72
            R = column[2] * 0.21

            weighted_sum = B + G + R

            column[0] = column[1] = column[2] = weighted_sum

    greyscale_image = image_array.astype("uint8")
    cv2.imwrite(filename + "_greyscale" + file_extension, greyscale_image)


# If run as a script: Time 3 runs and log to file
if __name__ == "__main__":
    my_times = []
    for i in range(3):
        tic = time.perf_counter()
        python_color2grey("rain.jpg")
        toc = time.perf_counter()
        duration = toc - tic
        my_times.append(duration)

    avg_time = sum(my_times)/len(my_times)

    with open("python_report_color2grey.txt", "w") as file:
        file.write(f"""Timing: python_color2grey
Dimensions: 400, 600, 3
Average runtime running python_color2grey after 3 runs: {avg_time:.2f} s
Timing performed using: time.perf_counter()""")

