import cv2
import numpy as np
from Utils import rescaleFrame

img = cv2.imread('input_img/cars.jpg')
img = rescaleFrame(img, .3)
cv2.imshow('Cars', img)

# Average, or median values of the surrounding pixels of a kernel center pixel

# Averaging
average = cv2.blur(img, (3,3))
cv2.imshow('Average Blur', average)

# Gaussian Blur
gauss = cv2.GaussianBlur(img, (3,3), 0)
cv2.imshow('Gaussian Blur', gauss)

# Median Blur
median = cv2.medianBlur(img, ksize=3) # normally ksize is not very high, normally 3
cv2.imshow('Median Blur', median)

# Bilateral Blur
# keep edges, blur the inside
# (smudged version of the image)
bilateral = cv2.bilateralFilter(img, d=30, sigmaColor=65, sigmaSpace=65)
cv2.imshow('Bilateral Blur', bilateral)

cv2.waitKey(0)