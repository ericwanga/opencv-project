import cv2
import numpy as np
from Utils import rescaleFrame
import matplotlib.pyplot as plt

img = cv2.imread('input_img/classroom1.jpg')
img = rescaleFrame(img, .75)
cv2.imshow('Cars', img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray', gray)

# Laplacian - 拉普拉斯算子 - pencil drawing-like edges - less in advanced usage
# pixel gradients
lap = cv2.Laplacian(gray, cv2.CV_64F)
lap = np.uint8(np.absolute(lap))
cv2.imshow('Laplacian', lap)

# Sobel - more in advanced usage
sobelx = cv2.Sobel(gray, cv2.CV_64F, dx=1, dy=0)
sobely = cv2.Sobel(gray, cv2.CV_64F, dx=0, dy=1)
combined_sobel = cv2.bitwise_and(sobelx, sobely)
cv2.imshow('Sobel X', sobelx)
cv2.imshow('Sobel Y', sobely)
cv2.imshow('Sobel Combined', combined_sobel)

canny = cv2.Canny(gray, 150, 175)
cv2.imshow('Canny Edge', canny)

cv2.waitKey(0)