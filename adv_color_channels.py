import cv2
import numpy as np
from Utils import rescaleFrame

img = cv2.imread('input_img/cars.jpg')
img = rescaleFrame(img, .3)
cv2.imshow('Cars', img)

b,g,r = cv2.split(img)

# color pixel concentration
# in each channel image, parts will be whiter/lighter for its corresponding color
cv2.imshow('Blue', b) # blue pixels concentrate to blue parts, hence whiter/lighter
cv2.imshow('Green', g) # green pixels concentrate to green parts, hence whiter/lighter
cv2.imshow('Red', r) # red parts will be whiter/lighter

print(img.shape)
print(b.shape)
print(g.shape)
print(r.shape)

# merge channels together
merged = cv2.merge([b,g,r])
cv2.imshow('Merged', merged)

# A way to only show single channel color, instead of grayscale ones
blank = np.zeros(img.shape[:2],dtype='uint8')

blue = cv2.merge([b, blank, blank])
green = cv2.merge([blank, g, blank])
red = cv2.merge([blank, blank, r])

cv2.imshow('Blue', blue) # lighter portion means concentration of this color pixels
cv2.imshow('Green', green)
cv2.imshow('Red', red)
# can merge these back to original image as well

cv2.waitKey(0)