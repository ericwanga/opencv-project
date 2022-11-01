import cv2
import time
import HumanPoseModule as pm
from Utils import position_mappings

# cap = cv2.VideoCapture('rtsp://192.168.0.80:9000/live')
# cap = cv2.VideoCapture('../../../recordings/lego_rover_build_44mins/video_20220716_44m_resize.mp4')
# cap = cv2.VideoCapture('../../../recordings/lego_rover_build_44mins/split/split000.mp4')
cap = cv2.VideoCapture('../../../recordings/lego_rover_build_44mins/split/split001.mp4')
# cap = cv2.VideoCapture('../../../recordings/lego_rover_build_44mins/split/split002.mp4')
# cap = cv2.VideoCapture('../../../recordings/lego_rover_build_44mins/split/split003.mp4')
# cap = cv2.VideoCapture('../../../recordings/lego_rover_build_44mins/split/split004.mp4')

# set "STATIC_IMAGE_MODE" to True, so person detection runs every input image
# otherwise False (default) will detect the most prominent person in the very first images
# and subsequently without invoking another detection until loses track
detector = pm.poseDetector(mode=True, detectionCon=0.5, trackCon=0.5)
pTime = 0
position = 16
positionname = position_mappings[position]

while True:
    success, img = cap.read()
    img = detector.findpose(img)
    lmList = detector.findposition(img, draw=False)

    # print(lmList)  # try this: all 33 positions
    # print(lmList[16])  # try this: right_wrist
    if len(lmList) != 0:
        print('Position {} {}: '.format(position, positionname), lmList[position])
        # overlay POI on existing landmarks
        cv2.circle(img, (lmList[position][1], lmList[position][2]), 10, (0, 0, 255), cv2.FILLED)

    # display fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, 'fps' + str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow('Image', img)
    key = cv2.waitKey(1)

    if key == 27:
        print('ESC pressed, break')
        break
