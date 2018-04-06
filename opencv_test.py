# coding=utf-8
import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib.patches import Circle
from matplotlib.pyplot import imshow, show

img = np.array(Image.open(sys.argv[1]))

img = cv2.medianBlur(img, 5)
cimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

color_threshold = 120
mask = img[:, :] > color_threshold
img[mask] = 0

imshow(img, cmap="gray")

canny_threshold = 30
center_threshold = 20
circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 40,
                           param1=canny_threshold, param2=center_threshold, minRadius=10, maxRadius=500)

circles = np.uint16(np.around(circles))
fig, ax = plt.subplots(1)

for i in circles[0, :]:
    # draw the outer circle
    cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
    # draw the center of the circle
    cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)

    circ = Circle((i[0], i[1]), i[2], fc='none', ec='red')
    ax.add_patch(circ)

imshow(img, cmap="gray")
show()
