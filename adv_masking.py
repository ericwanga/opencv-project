
import cv2
import numpy as np
from Utils import rescaleFrame

img = cv2.imread('input_img/cars.jpg')
img = rescaleFrame(img, .3)
cv2.imshow('Cars', img)

# AND, OR, XOR, NOT

blank = np.zeros(img.shape[:2], dtype='uint8')

# mask
# circle_mask = cv2.circle(blank, (img.shape[1]//2, img.shape[0]//2), 100, 255, -1)
# cv2.imshow('Circle Mask', circle_mask)

# masked = cv2.bitwise_and(img, img, mask=circle_mask)
# cv2.imshow('Masked Image', masked)

# shifted mask
circle = cv2.circle(blank.copy(), (img.shape[1]//2 +50, img.shape[0]//2), 100, 255, -1)
# cv2.imshow('Mask', circle)

# masked = cv2.bitwise_and(img, img, mask=mask)
# cv2.imshow('Masked Image', masked)

# create a weird shape mask
rectangle = cv2.rectangle(blank.copy(), pt1=(30,30), pt2=(300, 300), color=255, thickness=-1)
# circle = cv2.circle(blank.copy(), (200,200), 200, 255, -1)
# cv2.imshow('Rectangle', rectangle)
# cv2.imshow('Circle', circle)

# # bitwise OR - non-intersecting and intersecting regions
weird_shape_mask = cv2.bitwise_or(circle, rectangle)
print(img.shape, weird_shape_mask.shape) # size of mask needs to be same as image size

masked = cv2.bitwise_and(img, img, mask=weird_shape_mask)
cv2.imshow('Weird Shape Masked Image', masked)



cv2.waitKey(0)