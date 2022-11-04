import cv2
import numpy as np
from Utils import rescaleFrame

# img = cv2.imread('input_img/cars.jpg')
# img = rescaleFrame(img, .3)
# cv2.imshow('Cars', img)

# AND, OR, XOR, NOT

# pixel is turned on if value is 1, turned off if value is 0

blank = np.zeros((400,400), dtype='uint8')

rectangle = cv2.rectangle(blank.copy(), pt1=(30,30), pt2=(370, 370), color=255, thickness=-1)
circle = cv2.circle(blank.copy(), (200,200), 200, 255, -1)
cv2.imshow('Rectangle', rectangle)
cv2.imshow('Circle', circle)

# bitwise AND - intersecting regions
bitwise_and = cv2.bitwise_and(rectangle, circle)
cv2.imshow('Bitwise AND', bitwise_and)

# bitwise OR - non-intersecting and intersecting regions
bitwise_or = cv2.bitwise_or(rectangle, circle)
cv2.imshow('Bitwise OR', bitwise_or)

# bitwise XOR - non-intersecting regions
bitwise_xor = cv2.bitwise_xor(rectangle, circle)
cv2.imshow('Bitwise XOR', bitwise_xor)

# bitwise NOT - reverse the pixels
bitwise_not = cv2.bitwise_not(rectangle)
cv2.imshow('Rectangle NOT', bitwise_not)

cv2.waitKey(0)