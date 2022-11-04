import cv2
import numpy as np

# rescale frames, default to 75%
# if shrinking, use INTER_AREA
# if enlarging, use INTER_LINEAR, INTER_CUBIC
def rescaleFrame(frame, scale = 0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    if scale <= 1:
        interpolation = cv2.INTER_AREA # shrink
    else:
        interpolation = cv2.INTER_LINEAR # enlarge
    return cv2.resize(frame, dimensions, interpolation=interpolation)

# read image and resize it
img = cv2.imread('input_img/cars.jpg')
img = rescaleFrame(img, .3)
cv2.imshow('Cars', img)

# Enlarge
# note not to overload than resolution size
enlarged = rescaleFrame(img, 1.2)
# cv2.imshow('Enlarge', enlarged)

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow('Gray', gray)

# Blur
blur = cv2.GaussianBlur(src=img, ksize=(7, 7), sigmaX=cv2.BORDER_DEFAULT)
cv2.imshow('Blue', blur)

# Edge Cascade 1
canny = cv2.Canny(img, threshold1=125, threshold2=175)
# cv2.imshow('Edge Cascade', canny)

# Edge Cascade 2
canny_on_blur = cv2.Canny(blur, threshold1=125, threshold2=175)
# cv2.imshow('Edge Cascade on blur', canny_on_blur)

# Dilating the image
dilated = cv2.dilate(canny, (5, 5), iterations=3)
# cv2.imshow('Dialated', dilated)

# Eroding
eroded = cv2.erode(dilated, (5, 5), iterations=3)
# cv2.imshow('Eroded', eroded)

# Resize
# AREA for shrinking, LINEAR, CUBIC for enlarging
resized = cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA)
# cv2.imshow('Reseized', resized)

# Cropping
cropped = img[50:200, 200:400]
# cv2.imshow('Cropped', cropped)

# Flipping
flip = cv2.flip(img, -1)
# 0: vertically
# 1: horizontally
# -1: both
# cv2.imshow('Flip', flip)

# Translation (shift)
# -x --> left
# -y --> up
# x --> right
# y --> down
def translateFrame(img, x, y):
    transMat = np.float32([[1, 0, x], [0, 1, y]])
    dimensions = (img.shape[1], img.shape[0]) # width, height
    return cv2.warpAffine(img, transMat, dimensions)

translated = translateFrame(img, -100, 100)
# cv2.imshow('Translated', translated)

# Rotate
def rotateFrame(img, angle, rotPoint=None):
    (height, width) = img.shape[:2]
    # assume center
    if rotPoint is None:
        rotPoint = (width//2, height//2) # center
    rotMat = cv2.getRotationMatrix2D(rotPoint, angle, scale=1.0)
    dimensions = (width, height)
    return cv2.warpAffine(img, rotMat, dimensions)

rotated = rotateFrame(img, 45) # left rotate
# cv2.imshow('Rotated', rotated)

# if rotate a rotated image, will have blank area rotated as well
# can fix this by direct rotate to sum of the two rotation angles
rotated = rotateFrame(img, -90) # right rotate
# cv2.imshow('Rotated', rotated)

# rotate on a point
rotated_on_point = rotateFrame(img, -90, (150, 150))
# cv2.imshow('Rotated on a point', rotated_on_point)


# -----------------------------------

# Contours
# boundaries of objects
# contour != edge
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray', gray)

# edges on original
canny = cv2.Canny(img, 125, 175)
cv2.imshow('Canny Edges', canny)

# contours
# returned contours is a np list
# RETR_TREE: want hierarchy contours
# RETR_EXTERNAL: only want external contours
# RETR_LIST: all contours in the image
# CHAIN_APPROX: approximation of what the contours returned
# CHAIN_APPROX_NONE: no approximation, just return required contours
# CHAIN_APPROX_SIMPLE: return an approximation that makes sense, e.g. two points to approximate a line
contours, hierarchies = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
print(f'{len(contours)} contour(s) found! - contours APPROX_NONE - on original')
contours, hierarchies = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
print(f'{len(contours)} contour(s) found! - contours APPROX_SIMPLE - on original')

# edges on blur
blur = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT) # try use gray
cv2.imshow('Blur 2', blur)
# edges on blur
canny_on_blur = cv2.Canny(blur, 125, 175)
cv2.imshow('Canny Edges 2 on blur', canny_on_blur)
contours, hierarchies = cv2.findContours(canny_on_blur, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
print(f'{len(contours)} contour(s) found! - contours APPROX_SIMPLE - on blur')


# -------------------

# Threshold
# convert the image to binary: 0 or 1, black or white
ret, thresh = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY)
cv2.imshow('Threshold', thresh)
contours, hierarchies = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
print(f'{len(contours)} contour(s) found! - threshold - on gray')

# -------------------

# show draw contours on a blank image
blank = np.zeros(img.shape, dtype='uint8')
cv2.drawContours(blank, contours, contourIdx=-1, color=(0,0,255), thickness=1)
cv2.imshow('Contours Drawn', blank)


cv2.waitKey(0)