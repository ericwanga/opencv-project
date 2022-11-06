import os
import sys
import imageio as imageio
import cv2
import numpy as np
import time
from Utils import position_mappings

class TargetFormat(object):
    GIF = ".gif"
    MP4 = ".mp4"
    AVI = ".avi"

def convertFile(inputpath, targetFormat):

    outputpath = os.path.splitext(inputpath)[0] + targetFormat
    print('Converting\r\n\t{0}\r\nto\r\nt{1}'.format(inputpath, outputpath))

    reader = imageio.get_reader(inputpath)
    fps = reader.get_meta_data()['fps']

    writer = imageio.get_writer(outputpath, fps=10)
    for i, im in enumerate(reader):
        sys.stdout.write("frame {0}".format(i))
        sys.stdout.flush()
        writer.append_data(im)
    print('\nFinalizing...')
    writer.close()
    print('Done')

convertFile('output/output5.avi', TargetFormat.GIF)

# frames = []
# cap = cv2.VideoCapture('output/output5.avi')
#
# while True:
#     success, img = cap.read()
#     # frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     frames.append(img)
#
#     if cv2.waitKey(1) & 0xFF == 27:
#         print('ESC pressed, break')
#         break
#
# exportname = 'output/output5.gif'
# imageio.mimsave(exportname, frames, fps=10)
