import cv2
import numpy as np
from Utils import rescaleFrame
import matplotlib.pyplot as plt

img = cv2.imread('input_img/cars.jpg')
img = rescaleFrame(img, .3)
cv2.imshow('Cars', img)

# plt.imshow(img)
# plt.show()

# BGR to Grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow('Gray', gray)

# BGR to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
cv2.imshow('HSV', hsv)

# BGR to L+a+b
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
# cv2.imshow('LAB', lab)

# BGR to RGB
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# cv2.imshow('RGB', rgb)
# now cv2 shows opposite colors
# because cv is BGR by default, and we are asking it to show RGB

# try in plt to show the converted RGB image
# plt.imshow(rgb)
# now plt is showing normally,
# because plt is RGB by default, and it is RGB now
# plt.show()

# No direct conversion
# HSV to BGR
hsv_bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
cv2.imshow('HSV --> BGR', hsv_bgr)
# Graysclae to BGR to LAB



cv2.waitKey(0)