
# create a method which takes any 3 points as input, and returns the angle of the 3 points
# input 3 points of the arm, calculate the angle, and determine if arm is stretched open
# arm positions:
# 12 right_shoulder (11 left_shoulder)
# 14 right_elbow (13 left_elbow)
# 16 right_wrist (15 left_wrist)

import cv2
import numpy as np
import time
import HumanPoseModule as pm
from Utils import position_mappings

position = 16
print(position_mappings[position])

# cap = cv2.VideoCapture('../../../recordings/lego_rover_build_44mins/split/split000.mp4')
cap = cv2.VideoCapture('../../../recordings/lego_rover_build_44mins/split/split001.mp4')
# cap = cv2.VideoCapture('../../../recordings/lego_rover_build_44mins/split/split002.mp4')
# cap = cv2.VideoCapture('../../../recordings/lego_rover_build_44mins/split/split003.mp4')
# cap = cv2.VideoCapture('../../../recordings/lego_rover_build_44mins/split/split004.mp4')

detector = pm.poseDetector(mode=True, detectionCon=0.5, trackCon=0.5)
count = 0


# img = cv2.imread()
while True:
    success, img = cap.read()
    # img = cv2.resize(480, 480)
    img = detector.findpose(img, draw=False)
    lmList = detector.findposition(img, draw=False)
    # print(lmList)
    if len(lmList) != 0:
        # right arm
        angle_r = detector.findAngle(img, 12, 14, 16, True)
        # convert to percentage - check the tradeoff between range and accuracy
        # this is also a place to filter out noise poses
        per_r = np.interp(angle_r, (30, 179), (0, 100))  # from () to ()
        print('angle_right_arm {}, percentage {}'.format(angle_r, per_r))

        # TODO check: frontal facing, or sideways facing to the camera
        # by
        # if


        # TODO check: scanning (interaction with Viana), or assembling lego (self-work), or browsing lego from table (self-work)
        # scanning: percentage >= angle >= 120 AND duration is shorter than 3 seconds
        # assembling: angle <= 90 AND duration is longer than 3 seconds
        # other self-work: ELSE
        # if per_r >= 50:


        # left arm
        angle_l = detector.findAngle(img, 11, 13, 15, True)
        # convert to percentage - check tradeoff
        per_l = np.interp(angle_l, (30, 179), (0, 100))  # from () to ()
        print('angle_left_arm {}, percentage {}'.format(angle_l, per_l))

        # TODO: replicate same checks as right arm


    # img =
    cv2.imshow('Image', img)
    key = cv2.waitKey(1)

    if key == 27:
        print('ESC pressed, break')
        break


