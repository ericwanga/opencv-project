import cv2
import mediapipe as mp
import time

mpPose = mp.solutions.pose
mpDraw = mp.solutions.drawing_utils
pose = mpPose.Pose(static_image_mode=False  # default False
                   , model_complexity=1  # default 1
                   , smooth_landmarks=True  # default True
                   , enable_segmentation=False  # default False
                   , smooth_segmentation=True  # default False
                   , min_detection_confidence=0.5  # default 0.5
                   , min_tracking_confidence=0.5  # default 0.5
                   )  # check parameters

cap = cv2.VideoCapture('../../../recordings/lego_rover_build_44mins/video_20220716_44m_resize.mp4')
pTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    # print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for lm_id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            print(lm_id, lm)
            # get the pixel values from landmark values
            # to get this, need landmark ratio value (x or y or z) multiply with width (w)
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)  # overlay on previous dots

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow('Image', img)

    cv2.waitKey(1)
