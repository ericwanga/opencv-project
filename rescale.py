import cv2

# img = cv2.imread('')
# cv2.imshow('Image', img)

# rescale frames, default to 75%
def rescaleFrame(frame, scale = 0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

# reading video
# use the built-in webcam
#capture = cv2.VideoCapture(0)
# use external camera connected to USB port (LHS)
#capture = cv2.VideoCapture(2)
# use CISCO Meraki MV2 camera under the same wifi network via RTSP protocol
# obtain this RTSP link from Meraki Dashboard -> Camera -> Setting -> Enable RTSP
capture = cv2.VideoCapture("rtsp://192.168.0.80:9000/live")
while True:
    isTrue, frame = capture.read()

    frame_resized = rescaleFrame(frame, scale=.5)
    cv2.imshow('Video resized', frame_resized)

    cv2.imshow('Video', frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
#cv2.waitKey(0)