import cv2
import boto3
from botocore.client import Config
import time
import io

ACCESS_KEY_ID = ''
ACCESS_SECRET_KEY = ''
BUCKET_NAME = 'mv2bucket'
RTSP_LINK = 'rtsp://192.168.0.80:9000/live'
print(RTSP_LINK)

s3 = boto3.resource('s3',
                    aws_access_key_id=ACCESS_KEY_ID,
                    aws_secret_access_key=ACCESS_SECRET_KEY
                #   , config=Config(signature_version='s3v1')
                    )

# videoFile = "a.avi"
capture = cv2.VideoCapture(RTSP_LINK)
frame_width = int(capture.get(3))
frame_height = int(capture.get(4))
print(f'frame width: {frame_width}, frame height: {frame_height}')
frameRate = capture.get(5)  # frame rate
print('frameRate: ', frameRate)
print('Press ESC to quit')
c = -2
count = 1

# sometimes FPS becomes a false value (180000), need to restart the script
while capture.isOpened() and frameRate != 180000.0:
    try:
        frameId = capture.get(1)  # current frame number
        ret, frame = capture.read()
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)  # wait for 1ms

        if not ret:
            break

        # write 1 frame every 30 frames
        if frameId % frameRate == 0:
            c += 1
            # skip first 60 frames, and when
            if count < (frameId // 30) and c < 5 and key != 27:
                #if key != 27:
                    print(f'frameId: {frameId} frameRate: {frameRate} c: {c} count: {count}')
                    # write to local path
                    cv2.imwrite('output/frames/img{}-{}.jpg'.format(count, time.strftime("%Y%m%d-%H%M%S")), frame)

                    # write to s3 put_object as bytes file
                    s3.Bucket(BUCKET_NAME).put_object(Key='video/frames/img{}-{}.jpg'.format(count, time.strftime("%Y%m%d-%H%M%S")), Body=bytes(frame))

                    # another way to put file
                    out_img = io.BytesIO()
                    frame.save(out_img, 'jpg')
                    out_img.seek(0)
                    #s3.Bucket(BUCKET_NAME).put_object(Key='video/frames/img{}-{}.jpg'.format(count, time.strftime("%Y%m%d-%H%M%S")), Body=out_img)

                    count += 1

        if key == 27:
            print('ESC pressed, break')
            break
    except AttributeError:
        print('Exception error occurred ...')
        pass


capture.release()
cv2.destroyAllWindows()
print("Done!")

