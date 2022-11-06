import os
import sys
import numpy as np
import math
import time
import matplotlib.pyplot as plt

from PIL import Image
import cv2
import mediapipe as mp
from mediapipe.python.solutions import pose as mp_pose
import torch


def findposition(results, img, draw=True):
    lmList = []
    # if results are available
    if results.pose_landmarks:
        for lm_id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            # print(lm_id, lm)
            # lm contains id, x,y,z, visibility score.
            # x,y,z are ratios, to get the pixel values from landmark values,
            # need to multiply landmark ratios (x or y) with image shape (w or h)
            cx, cy = int(lm.x * w), int(lm.y * h)
            # can choose what fields to be stored. Here just include all 5 available fields
            lmList.append([lm_id, cx, cy, round(lm.z, 5), round(lm.visibility, 7)])
            if draw:
                # overlay on existing dots
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

    return lmList

def findAngle(lmList, img, p1, p2, p3, draw=True):
    # get landmarks
    x1, y1 = lmList[p1][1:3]
    x2, y2 = lmList[p2][1:3]
    x3, y3 = lmList[p3][1:3]

    # calculate angle (convert radians to degrees)
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    if angle < 0:  # if negative angle value, convert to positive
        angle += 360
    if angle > 180:
        angle = 360 - angle

    # print('Angle:', angle)

    # draw
    if draw:
        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)  # white line
        cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 2)  # white line
        cv2.circle(img, (x1, y1), 8, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x1, y1), 12, (0, 0, 255), 1)
        cv2.circle(img, (x2, y2), 8, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 12, (0, 0, 255), 1)
        cv2.circle(img, (x3, y3), 8, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x3, y3), 12, (0, 0, 255), 1)
        cv2.putText(img, str(int(angle)), (x2 - 35, y2 + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)

    return angle

# Model
yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
# yolo_model = torch.load('yolov5s.pt')

yolo_model.classes = [0]

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# run locally
# cap = cv2.VideoCapture('../../../recordings/lego_rover_build_44mins/split/split000.mp4')
cap = cv2.VideoCapture('../../../recordings/lego_rover_build_44mins/split2/split005.mp4')
# cap = cv2.VideoCapture('../../../recordings/lego_rover_build_44mins/split2/split008.mp4')
# cap = cv2.VideoCapture('../../../recordings/lego_rover_build_44mins/split2/split010.mp4')
# cap = cv2.VideoCapture('../../../recordings/lego_rover_build_44mins/split2/split015.mp4')

# run in google colab
# cap = cv2.VideoCapture('/content/drive/MyDrive/U/phd/work4_openvino/recordings/lego_rover_build_44mins/split10s/split001.mp4')

while cap.isOpened():
    success, frame = cap.read()
    h, w, _ = frame.shape
    size = (w, h)
    print(size)
    break

# webcam
# cap = cv2.VideoCapture(0)

# run locally
# save video file as output.avi
out = cv2.VideoWriter('output/output_2min.avi', cv2.VideoWriter_fourcc(*"MJPG"), 20, size)

# run in google colab
# save video file as output.avi
out = cv2.VideoWriter('/content/drive/MyDrive/U/phd/work4_openvino/PycharmProjects/projectCV/HumanPoseEstimation/output/output5.avi',
                     cv2.VideoWriter_fourcc(*"MJPG"), 20, size)


count_r = 0
count_l = 0
pTime = 0
dir_r = 0
dir_l = 0
frames = []
arm_count = {}

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # recolor
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # make image writable to False to improve prediction performance
    image.flags.writeable = False

    result = yolo_model(image)

    # recolor image back to BGR for rendering
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    print(result.xyxy)

    img_list = []
    MARGIN = 15

    for idx, (xmin, ymin, xmax, ymax, confidence, clas) in enumerate(result.xyxy[0].tolist()):
        if idx == 0:
            pstart = 300
            pend = 400
        elif idx == 1:
            pstart = 450
            pend = 550
        elif idx == 2:
            pstart = 600
            pend = 700
        else:
            pstart = 0
            pend = 0

        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            # pose prediction
            image_crop = image[int(ymin) + MARGIN:int(ymax) + MARGIN, int(xmin) + MARGIN:int(xmax) + MARGIN:]
            # results = pose.process(image[int(ymin)+MARGIN:int(ymax)+MARGIN, int(xmin)+MARGIN:int(xmax)+MARGIN:])
            results = pose.process(image_crop)

            # draw landmarks
            mp_drawing.draw_landmarks(
                image[int(ymin) + MARGIN:int(ymax) + MARGIN, int(xmin) + MARGIN:int(xmax) + MARGIN:],
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                )

            # img = findpose(img, draw=False)
            lmList = findposition(results, image_crop, draw=False)

            if len(lmList) != 0:
                # right arm
                angle_r = findAngle(lmList, image_crop, 12, 14, 16, True)
                # convert to percentage - check the tradeoff between range and accuracy
                # this is also a place to filter out noise poses
                per_r = np.interp(angle_r, (30, 180), (0, 100))  # from () to ()
                # bar_r = np.interp(angle_r, (30, 170), (300, 400)) # use angle
                # bar_r = np.interp(per_r, (40, 100), (300, 400))  # use percentage
                bar_r = np.interp(per_r, (30, 100), (pstart, pend))  # use percentage
                print('angle_right_arm {}, percentage {}'.format(angle_r, per_r))

                # left arm
                angle_l = findAngle(lmList, image_crop, 11, 13, 15, True)
                # convert to percentage - check tradeoff
                per_l = np.interp(angle_l, (30, 180), (0, 100))  # from () to ()
                # bar_l = np.interp(angle_l, (30, 170), (300, 400)) # use angle
                # bar_l = np.interp(per_l, (40, 100), (300, 400))  # use percentage
                bar_l = np.interp(per_l, (30, 100), (pstart, pend))
                print('angle_left_arm {}, percentage {}'.format(angle_l, per_l))

                # TODO: replicate same checks as right arm
                color = (255, 0, 0)  # blue

                # right arm
                if per_r >= 90:
                    color = (0, 255, 0)  # green
                    if dir_r == 0:
                        count_r += 0.5
                        dir_r = 1
                if per_r <= 30:
                    color = (255, 0, 0)  # blue
                    if dir_r == 1:
                        count_r += 0.5
                        dir_r = 0

                # left arm
                if per_l >= 90:
                    color = (0, 255, 0)  # green
                    if dir_l == 0:
                        count_l += 0.5
                        dir_l = 1
                if per_l <= 30:
                    color = (255, 0, 0)  # blue
                    if dir_l == 1:
                        count_l += 0.5
                        dir_l = 0

                print(count_l, count_r)
                count = {'L': count_l, 'R': count_r}
                arm_count.update({idx: {'count': count}})

                # use average percentage as bar value
                bar_avg = np.mean((bar_l, bar_r))

                # count_l_total = int(np.sum([arm_count[i]['count']['L'] for i in range(0, len(arm_count))]))
                # count_r_total = int(np.sum([arm_count[i]['count']['R'] for i in range(0, len(arm_count))]))

                # display arm counts
                # cv2.rectangle(image, (300, 25), (400, 50), color, 2)
                # cv2.rectangle(image, (300, 25), (int(bar_avg), 50), color, cv2.FILLED)
                # cv2.putText(image, 'L {} R {}'.format(count_l, count_r), (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

                # cv2.rectangle(image, (pstart, 25), (pend, 50), color, 2)
                cv2.rectangle(image, (pstart, 25), (pend, 50), color, 2)
                cv2.rectangle(image, (pstart, 25), (int(bar_avg), 50), color, cv2.FILLED)
                # cv2.putText(image, 'L {} R {}'.format(count_l, count_r), (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        if idx != 3:
            count_l_total = int(np.mean([arm_count[i]['count']['L'] for i in range(0, len(arm_count))]))
            count_r_total = int(np.mean([arm_count[i]['count']['R'] for i in range(0, len(arm_count))]))
            cv2.putText(image, f"Arms reaching out L {count_l_total} R {count_r_total}", (25, 50),
                        cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)

        # display fps
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        # cv2.putText(image, 'FPS {}'.format(str(int(fps))), (50, 100), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)

        img_list.append(image[int(ymin):int(ymax), int(xmin):int(xmax):])

        # cv2.imshow('Image', image)
        # cv2_imshow(image)

        # write to video file
        out.write(image)

        # cv2.imshow('Activity recognition', image)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break

cap.release()
out.release()
cv2.destroyAllWindows()
