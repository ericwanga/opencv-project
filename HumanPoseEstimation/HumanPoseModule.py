import cv2
import mediapipe as mp
import math
import time
from Utils import position_mappings

class poseDetector():

    # initializations
    def __init__(self, mode=False, complexity=1, smoothLm=True, enableSeg=False, smoothSeg=True,
                 detectionCon=0.5, trackCon=0.5):
        """
        mode ("STATIC_IMAGE_MODE"): default to False, the solution treats the input images as a video stream.
        It will try to detect the most prominent person in the very first images,
        and upon a successful detection further localizes the pose landmarks. In subsequent images,
        it then simply tracks those landmarks without invoking another detection until it loses track,
        on reducing computation and latency. If set to true, person detection runs every input image,
        ideal for processing a batch of static, possibly unrelated, images
        """
        # check these parameters in .conda/envs/projectCV/.../site-packages/mediapipe/python/solutions/pose.py
        # or command+click .Pose()
        self.mode = mode
        self.complexity = complexity
        self.smoothLm = smoothLm
        self.enableSeg = enableSeg
        self.smoothSeg = smoothSeg
        self.detectCon = detectionCon
        self.trackCon = trackCon

        self.mpPose = mp.solutions.pose
        self.mpDraw = mp.solutions.drawing_utils
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smoothLm
                                     , self.enableSeg, self.smoothSeg, self.detectCon, self.trackCon)

    # create a method to find the pose
    def findpose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        # print(self.results.pose_landmarks)

        # if results are available
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img

    # find total 33 positions' data and store in a list
    def findposition(self, img, draw=True):
        self.lmList = []
        # if results are available
        if self.results.pose_landmarks:
            for lm_id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(lm_id, lm)
                # lm contains id, x,y,z, visibility score.
                # x,y,z are ratios, to get the pixel values from landmark values,
                # need to multiply landmark ratios (x or y) with image shape (w or h)
                cx, cy = int(lm.x * w), int(lm.y * h)
                # can choose what fields to be stored. Here just include all 5 available fields
                self.lmList.append([lm_id, cx, cy, round(lm.z, 5), round(lm.visibility, 7)])
                if draw:
                    # overlay on existing dots
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        return self.lmList

    # calculate angle between 3 positions
    def findAngle(self, img, p1, p2, p3, draw=True):

        # get landmarks
        x1, y1 = self.lmList[p1][1:3]
        x2, y2 = self.lmList[p2][1:3]
        x3, y3 = self.lmList[p3][1:3]

        # calculate angle (convert radians to degrees)
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle < 0:  # if negative angle value, convert to positive
            angle += 360
        print('Angle:', angle)

        # draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)  # white line
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 2)  # white line
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 1)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 1)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 1)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        return angle


def main():
    '''
    testing script of main. This won't be run if only calling the class's methods
    :return:
    '''
    cap = cv2.VideoCapture('../../../recordings/lego_rover_build_44mins/video_20220716_44m_resize.mp4')
    pTime = 0
    position = 16
    positionname = position_mappings[position]
    detector = poseDetector()

    while True:
        success, img = cap.read()
        img = detector.findpose(img)
        lmList = detector.findposition(img, draw=False)
        # print(lmList)  # try this: all 33 positions
        # print(lmList[16])  # try this: right_wrist
        if len(lmList) != 0:
            print('Position {} {} '.format(position, positionname), lmList[position])
            cv2.circle(img, (lmList[position][1], lmList[position][2]), 10, (0, 0, 255), cv2.FILLED)  # overlay on previous dots

        # display fps
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, 'fps'+str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

        cv2.imshow('Image', img)
        key = cv2.waitKey(1)

        if key == 27:
            print('ESC pressed, break')
            break


if __name__ == "__main__":
    main()
