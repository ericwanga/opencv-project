from threading import Thread
import cv2
import boto3
from botocore.client import Config


class RTSPVideoWriterObject(object):
    def __init__(self, src=0):
        # Create a VideoCapture object
        self.capture = cv2.VideoCapture(src)

        # Default resolutions of the frame are obtained (system dependent)
        self.frame_width = int(self.capture.get(3))
        self.frame_height = int(self.capture.get(4))
        print(self.frame_width, self.frame_height)

        # Set up codec and output video settings
        #self.codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        self.codec = cv2.VideoWriter_fourcc(*'mp4v')
        #self.output_video = cv2.VideoWriter('output/output2.avi', self.codec, 10, (self.frame_width, self.frame_height))
        self.output_video = cv2.VideoWriter('output/output_RTSP_ThreadWriter.mp4', self.codec, 20, (self.frame_width, self.frame_height), True)

        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()

    def show_frame(self):
        # Display frames in main program
        if self.status:
            cv2.imshow('frame', self.frame)

        # Press Q on keyboard to stop recording
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            self.output_video.release()
            cv2.destroyAllWindows()
            exit(1)

    def save_frame(self):
        # Save obtained frame into video output file
        self.output_video.write(self.frame)


if __name__ == '__main__':

    ACCESS_KEY_ID = 'AKIA5AI5EJI55CMNKYOE'
    ACCESS_SECRET_KEY = '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'
    BUCKET_NAME = 'mv2bucket'
    RTSP_LINK = 'rtsp://192.168.0.80:9000/live'
    print(RTSP_LINK)

    s3 = boto3.resource('s3',
                        aws_access_key_id=ACCESS_KEY_ID,
                        aws_secret_access_key=ACCESS_SECRET_KEY,
                        config=Config(signature_version='s3v1')
                        )

    video_stream_widget = RTSPVideoWriterObject(RTSP_LINK)
    while True:
        try:
            video_stream_widget.show_frame()
            video_stream_widget.save_frame()
        except AttributeError:
            pass