
# create a method which takes any 3 points as input, and returns the angle of the 3 points
# input 3 points of the arm, calculate the angle, and determine if arm is stretched open
# arm positions:
# 12 right_shoulder (11 left_shoulder)
# 14 right_elbow (13 left_elbow)
# 16 right_wrist (15 left_wrist)

import cv2
import imageio as imageio
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
count_r = 0
count_l = 0
dir_r = 0
dir_l = 0
pTime = 0
frames = []

# img = cv2.imread()
while True:
    success, img = cap.read()
    # img = cv2.resize(img, (480, 240))
    img = detector.findpose(img, draw=False)
    lmList = detector.findposition(img, draw=False)
    # print(lmList)
    if len(lmList) != 0:
        # right arm
        angle_r = detector.findAngle(img, 12, 14, 16, True)
        # convert to percentage - check the tradeoff between range and accuracy
        # this is also a place to filter out noise poses
        per_r = np.interp(angle_r, (30, 170), (0, 100))  # from () to ()
        # bar_r = np.interp(angle_r, (30, 170), (300, 400)) # use angle
        bar_r = np.interp(per_r, (40, 100), (300, 400)) # use percentage
        print('angle_right_arm {}, percentage {}'.format(angle_r, per_r))

        # TODO check: frontal facing, or sideways facing to the camera
        # by
        # if

        # left arm
        angle_l = detector.findAngle(img, 11, 13, 15, True)
        # convert to percentage - check tradeoff
        per_l = np.interp(angle_l, (30, 170), (0, 100))  # from () to ()
        # bar_l = np.interp(angle_l, (30, 170), (300, 400)) # use angle
        bar_l = np.interp(per_l, (40, 100), (300, 400)) # use percentage
        print('angle_left_arm {}, percentage {}'.format(angle_l, per_l))

        # TODO check: scanning (interaction with Viana), or assembling lego (self-work), or browsing lego from table (self-work)
        # scanning: percentage >= angle >= 120 AND duration is shorter than 3 seconds
        # assembling: angle <= 90 AND duration is longer than 3 seconds
        # other self-work: ELSE
        # if per_r >= 50:

        # TODO: replicate same checks as right arm
        color = (255, 0, 0) # blue

        # right arm
        if per_r >= 80:
            color = (0, 255, 0) # green
            if dir_r == 0:
                count_r += 0.5
                dir_r = 1
        if per_r <= 40:
            color = (255, 0, 0) # blue
            if dir_r == 1:
                count_r += 0.5
                dir_r = 0

        # left arm
        if per_l >= 80:
            color = (0, 255, 0) # green
            if dir_l == 0:
                count_l += 0.5
                dir_l = 1
        if per_l <= 40:
            color = (255, 0, 0) # blue
            if dir_l == 1:
                count_l += 0.5
                dir_l = 0

        print(count_r, count_l)

        # use average percentage as bar value
        bar_avg = np.mean((bar_r, bar_l))

        # display arm counts
        cv2.rectangle(img, (300, 25), (400, 50), color, 2)
        cv2.rectangle(img, (300, 25), (int(bar_avg), 50), color, cv2.FILLED)
        cv2.putText(img, 'R {} L {}'.format(count_r, count_l), (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        # display fps
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, 'FPS {}'.format(str(int(fps))), (50, 90), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)



    cv2.imshow('Image', img)
    key = cv2.waitKey(1)

    frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    frames.append(frame)

    # img =
    if key & 0xFF == 27:
        print('ESC pressed, break')
        break

cap.release()
cv2.destroyAllWindows()

# convert to gif
with imageio.get_writer("gifs/highlevel.gif", mode="I") as writer:
    for idx, frame in enumerate(frames):
        writer.append_data(frame)

