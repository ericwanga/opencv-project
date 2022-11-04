import cv2
import numpy as np
from Utils import rescaleFrame
import matplotlib.pyplot as plt

img = cv2.imread('input_img/cars.jpg')
img = rescaleFrame(img, .3)
cv2.imshow('Cars', img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray', gray)

# Simple Thresholding
threshold, thresh = cv2.threshold(gray, thresh=100, maxval=255, type=cv2.THRESH_BINARY)
cv2.imshow('Simple Thresholded', thresh)

# inverse
threshold, thresh_inv = cv2.threshold(gray, thresh=100, maxval=255, type=cv2.THRESH_BINARY_INV)
cv2.imshow('Simple Thresholded Inverse', thresh_inv)


# --------------------------

# Adaptive Thresholding
# not maually set thresh
adaptive_thresh = cv2.adaptiveThreshold(gray, 255,
                                        adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
                                        thresholdType=cv2.THRESH_BINARY,
                                        blockSize=11,
                                        C=9) # try this value
cv2.imshow('Adaptive Thresholding', adaptive_thresh)


adaptive_thresh = cv2.adaptiveThreshold(gray, 255,
                                        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        thresholdType=cv2.THRESH_BINARY,
                                        blockSize=11,
                                        C=9)
cv2.imshow('Adaptive Thresholding Gaussian Adaptive', adaptive_thresh)


cv2.waitKey(0)