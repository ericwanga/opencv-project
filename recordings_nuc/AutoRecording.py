# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
from datetime import datetime, timedelta
from pytz import timezone
import subprocess
import cv2
import os
import keyboard
import gc

gc.collect()


# get datetime and timezone info to pass to folder and file name
def get_date_hmsz(time_zone, time_gap):
    current_time = datetime.now(timezone(time_zone))
    last_hour_from = current_time + timedelta(hours=time_gap * -1)
    last_hour_from_str = last_hour_from.strftime('%Y-%m-%d %H:%M:%S%z')
    return last_hour_from_str[0:22] + ':' + last_hour_from_str[-2:]


# call batch script to start recording
def recording_start(rtsp_url, script_path, output_path, output_filename):
    return subprocess.Popen(
        ['cmd', '/c', os.path.join(script_path, 'record_all.bat'), rtsp_url, output_path, output_filename])


# call batch script to capture frames
def capture_video_frames(script_path, file, output_path):
    # call batch script to start capture
    return subprocess.run(
        ['cmd', '/c', os.path.join(script_path, 'video_frame_capture_from_file.bat'), file, output_path])


# call batch script to extract audio and save to wav format
def extract_audio_wav(script_path, file, output_path, output_filename):
    # call batch script to start capture
    return subprocess.run(
        ['cmd', '/c', os.path.join(script_path, 'extract_audio_wav.bat'), file, output_path, output_filename])


# command to kill process by PID
def kill_recording(process):
    command = ['TASKKILL', '/F', '/T', '/PID', str(process.pid)]
    subprocess.call(command)


# get rtsp link and time duration from user input
def get_rtsp_and_time_duration_from_user():
    while True:
        # get rtsp link
        os.system('cls')
        predefined_rtsp = "rtsp://192.168.0.80:9000/live"
        print("Check:\nINFO: current RTSP link is {}\nPress [ENTER] to continue, press [c] to change".format(
            predefined_rtsp))
        if keyboard.read_key() == 'Enter':
            RTSP_URL_CAM1 = predefined_rtsp
        elif keyboard.read_key() == 'c':
            RTSP_URL_CAM1 = input("\nChange RTSP link to: ")
        else:
            RTSP_URL_CAM1 = predefined_rtsp

        if RTSP_URL_CAM1[:7] != 'rtsp://':
            print("ERROR: Invalid RTSP link, rtsp link start with 'rtsp://', please try again")
            continue

        # get time duration
        number = False
        while not number:
            print("Set recording duration (minutes): ")
            timeout = input()
            try:
                timeout = int(timeout)
                number = True
            except EOFError:
                pass
            except ValueError:
                print("\nPlease input an integer value as recording duration")
                pass

        # check and continue
        print('\n-----------------------------------------------------------------------------------------------------')
        print('Confirm:\nRTSP link: {}'.format(RTSP_URL_CAM1))
        print('Recording duration: {} minute(s)\n'.format(timeout))
        print("\nPress [Enter] to start recording, press [c] to change")
        if keyboard.read_key() == 'c':
            continue
        elif keyboard.read_key() == 'Enter':
            break
        else:
            break

    return RTSP_URL_CAM1, timeout


# set script path
SCRIPT_PATH = r"C:\Users\ericw.DESKTOP-ST5F8PV.000\Desktop\recordings"

# get rtsp link and time duration
RTSP_URL_CAM1, timeout = get_rtsp_and_time_duration_from_user()
print('INFO: rtsp link: {}'.format(RTSP_URL_CAM1))
print('INFO: time duration set to: {} minutes'.format(timeout))

# make output filename
last_date_from_str = get_date_hmsz('Australia/Adelaide', 0)
OUTPUT_FILENAME = last_date_from_str.replace(' ', '-').replace(':', '-').replace('+', '_')

# set output path
OUTPUT_PATH = os.path.join(SCRIPT_PATH, OUTPUT_FILENAME)
print('INFO: OUTPUT_PATH: {}'.format(OUTPUT_PATH))

# instantiate
capture = cv2.VideoCapture(RTSP_URL_CAM1)

if __name__ == '__main__':

    # 1. record video
    while True:
        # if camera RTSP stream is not connected, wait and retry
        if not capture.isOpened():
            print('Error opening video stream. Retry after 10 seconds')
            time.sleep(10)
            continue

        # if camera connected
        if capture.isOpened():
            print('INFO: camera connected\n')
            proc_recording = recording_start(rtsp_url=RTSP_URL_CAM1
                                             , script_path=SCRIPT_PATH
                                             , output_path=OUTPUT_PATH
                                             , output_filename=OUTPUT_FILENAME)

            # start recording for "timeout" minutes
            try:
                print('\n---------------------------------------------------------------------------------------------')
                print('INFO: start recording\n')
                proc_recording.communicate(timeout=timeout * 60)
            # when time's up, catch the "TimeoutExpired" exception
            except subprocess.TimeoutExpired:
                # kill the recording process
                print('{} minutes finished, stop the recording process: {}\n'.format(timeout, proc_recording.pid))
                kill_recording(proc_recording)

            print('INFO: jobs complete')
            print('INFO: recording and frame files saved at {}\n'.format(OUTPUT_PATH))
            break

    # 2. capture frames
    print('\n---------------------------------------------------------------------------------------------------------')
    print('INFO: start capturing frames')
    VID_FILE = os.path.join(OUTPUT_PATH + '_video', OUTPUT_FILENAME + '.ts')
    print('FILE: {}'.format(VID_FILE))
    capture_video_frames(script_path=SCRIPT_PATH, file=VID_FILE, output_path=OUTPUT_PATH)

    # 3. extract audio (wav)
    print('\n---------------------------------------------------------------------------------------------------------')
    print('INFO: start extracting audio wav file')
    VID_FILE = os.path.join(OUTPUT_PATH + '_video', OUTPUT_FILENAME + '.ts')
    print('FILE: {}'.format(VID_FILE))
    extract_audio_wav(script_path=SCRIPT_PATH, file=VID_FILE, output_path=OUTPUT_PATH, output_filename=OUTPUT_FILENAME)

    # finish
    print("\nTasks completed. All files are saved at: {}\nYou can now close CMD window(s) to exit.".format(SCRIPT_PATH))
