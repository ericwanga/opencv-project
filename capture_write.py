import numpy as np
import cv2

# rescale frames, default to 75%
def rescaleFrame(frame, scale = 0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

#cap = cv.VideoCapture(0)
cap = cv2.VideoCapture("rtsp://192.168.0.80:9000/live")
width = int(cap.get(3)) # 1920
height = int(cap.get(4)) # 1080

# Define codec and create VideoWriter object
#fourcc = cv.VideoWriter_fourcc('M', 'J', 'P', 'G')
#fourcc = cv.VideoWriter_fourcc('X', 'V', 'I', 'D')
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output/output_capture_write.mp4', fourcc, 10.0, (width, height), True)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # do something to the frame
    #frame = cv2.flip(frame, 0)
    #frame = cv2.cvtColor(frame, cv.COLOR_BGR2GRAY) # EMPTY OUTPUT FILE
    #frame = rescaleFrame(frame, scale=.75)

    # write the frame
    out.write(frame)
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()