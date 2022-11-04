import cv2
import numpy as np
from Utils import rescaleFrame
import matplotlib.pyplot as plt

img = cv2.imread('input_img/classroom1.jpg')
img = rescaleFrame(img, .3)
cv2.imshow('Cars', img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray', gray)

# Grayscale histogram
# gray_hist = cv2.calcHist([gray], channels=[0], mask=None, histSize=[256], ranges=[0,256])
# plt.figure()
# plt.title('Grayscale Histogram')
# plt.xlabel('Bins')
# plt.ylabel('# of pixels')
# plt.plot(gray_hist)
# plt.xlim([0, 256])
# plt.show()

# apply mask
# blank = np.zeros(img.shape[:2], dtype='uint8')
# # circle = cv2.circle(blank, (img.shape[1]//2, img.shape[0]//2), 150, 255, -1)
# rectangle = cv2.rectangle(blank.copy(), pt1=(5,30), pt2=(400, 300), color=255, thickness=-1)
# mask = cv2.bitwise_and(gray, gray, mask=rectangle)
# cv2.imshow('Mask', mask)
# gray_mask_hist = cv2.calcHist([gray], channels=[0], mask=mask, histSize=[256], ranges=[0,256])

# plt.figure()
# plt.title('Masked Grayscale Histogram')
# plt.xlabel('Bins')
# plt.ylabel('# of pixels')
# plt.plot(gray_mask_hist)
# plt.xlim([0, 256])
# plt.show()


# -------------------------

# color histogram
blank = np.zeros(img.shape[:2], dtype='uint8')
# circle = cv2.circle(blank, (img.shape[1]//2, img.shape[0]//2), 150, 255, -1)
rectangle = cv2.rectangle(blank.copy(), pt1=(5,30), pt2=(400, 300), color=255, thickness=-1)
mask = cv2.bitwise_and(img, img, mask=rectangle) # now this mask is 3-channel
cv2.imshow('Mask', mask)

plt.figure()
plt.title('Color Histogram')
plt.xlabel('Bins')
plt.ylabel('# of pixels')
colors = ('b', 'g', 'r')
for i, col in enumerate(colors):
    hist = cv2.calcHist([img], [i], rectangle, [256], [0, 256]) # use rectangle not 3-channel mask
    plt.plot(hist, color=col)
    plt.xlim([0, 256])
plt.show()

cv2.waitKey(0)