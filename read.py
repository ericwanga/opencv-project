import cv2

# reading video from webcam or external cameras
# pass in 0: webcam
#capture = cv2.VideoCapture(0)
# 2: external camera connected to USB port (LHS) of the laptop
#capture = cv2.VideoCapture(2)
capture = cv2.VideoCapture("rtsp://192.168.0.80:9000/live")

while True:
    isTrue, frame = capture.read()
    cv2.imshow('Video', frame)

    # press "q" on keyboard to exit
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()

# cv2.waitKey(0)
