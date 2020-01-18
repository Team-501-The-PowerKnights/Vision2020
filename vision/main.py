import cv2
import time
import sys
import logging
from util.config import run_config
from util.stopwatch import stopwatch as SW
from networktables import NetworkTables as NT
import find_target as FT
import socket
import numpy as np

logging.basicConfig(level=logging.DEBUG)

# the parameters passed into run_config are the configuration and the filename.
os, camera_location, calibration, freqFramesNT, address = run_config(None, None)


def main():
    camera_table = nt_init(address)
    cap = cap_init(camera_location)
    rect_cnt1, rect_cnt2 = create_rect(calibration['debug'])
    run(cap, camera_table, calibration, freqFramesNT, rect_cnt1, rect_cnt2)


def nt_init(robot_address):
    """
    Initialize network tables
    :parameter robot address
    :return camera network table
    """
    bot_address_found = False
    while not bot_address_found:
        try:
            robot_ip = None
            robot_ip = socket.gethostbyname(robot_address)  # determine robot IP
            if robot_ip is not None:
                print("INFO: Found robot at " + robot_ip)
                bot_address_found = True
        except socket.gaierror:
            print("WARNING: Unable to find robot IP Address.")  # this will loop until we find the robot
            continue

    nt_init = False
    while not nt_init:
        try:
            NT.initialize(server=robot_ip)  # initialize client
        except:
            continue  # this will loop until we connect to the robot
        try:
            vision_table = NT.getTable('SmartDashboard')
        except:
            NT.stop()
            NT.destroy()
            continue
        vision_table.putBoolean('connected', True)
        pullback = vision_table.getBoolean('connected', None)
        if pullback:
            nt_init = True
        else:
            continue
    else:
        return vision_table


def create_rect(debug):
    """
        Creates a rectangle and performs appropriate processing to provide a target
        returns the contour object of the rectangle
        :return the two contours of the rectangle we want to validate targets
        against (returned as a tuple)
        """
    # Draw rectangles of the retro reflective tape (Find dimensions in the game manual)
    # Camera dimensions: 320 x 240
    # Rectangle dimensions: 40 x 110
    if debug:
        timer_rect = SW('rect')
        timer_rect.start()
    width = 40
    length = 110
    img_width = 175
    img_length = 175

    top_left_x = int(img_width - width / 2)
    top_left_y = int(img_length - length / 2)
    bottom_right_x = int(img_width + width / 2)
    bottom_right_y = int(img_length + length / 2)

    background = np.zeros((350, 350, 3), np.uint8)
    rect1 = cv2.rectangle(background, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (255, 255, 255), -1)
    m = cv2.getRotationMatrix2D((350 / 2, 350 / 2), -14.5, 1)
    rect1_rotated = cv2.warpAffine(rect1, m, (350, 350))
    ret, thresh = cv2.threshold(rect1_rotated, 127, 255, cv2.THRESH_BINARY)
    thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt1 = contours[0]

    rect2 = rect1
    m = cv2.getRotationMatrix2D((350 / 2, 350 / 2), 14.5, 1)
    rect2_rotated = cv2.warpAffine(rect2, m, (350, 350))
    ret, thresh = cv2.threshold(rect2_rotated, 127, 255, cv2.THRESH_BINARY)
    thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt2 = contours[0]
    if debug:
        elapsed = timer_rect.get()
        print('DEBUG: rectangles took ' + str(elapsed))
    return cnt1, cnt2


def nt_send(camera_table, angle, valid_count, valid_update):
    """
    Send relevant data to the network table
    :param camera_table: camera network table
    :param angle: angle to target
    :param valid_count: number of valid updates we have found
    :param valid_update: boolean True if valid target found, false otherwise
    :return: None
    Vision.angle (double)
    Vision.locked (boolean)
    Vision.count (integer)
    """

    camera_table.putNumber("Vision.angle", angle)
    camera_table.putBoolean("Vision.locked", valid_update)
    camera_table.putNumber("Vision.count", valid_count)


def cap_init(camera_location):
    """
    Initialize camera
    :param camera_location: what the camera url is
    :return: cap returned from cv2.VideoCapture
    """
    try:
        cap = cv2.VideoCapture(eval(camera_location))
        time.sleep(1)
    except:
        print("Exception on VideoCapture init. Dying")
        sys.exit()
    return cap


def run(cap, camera_table, calibration, freqFramesNT, rect_cnt1, rect_cnt2):
    """
    Run the main vision algorithm on each camera frame and update network table appropriately
    :param cap: cap returned from cv2.VideoCapture
    :param camera_table: the network table we are writing to
    :param calibration: dictionary containing hsv thresholds and whether we are in debug mode or not
    :param freqFramesNT: frequency of frames for data to be sent to network tables
    :param rect_cnt: contour of the rectangle we want to validate targets against
    :return: None
    """
    valid_count = 0
    n = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            try:
                if calibration['debug']:
                    timer_fv=SW('FV')
                    timer_fv.start()
                angle, valid_update = FT.find_valids(frame, calibration, rect_cnt1, rect_cnt2)
                if calibration['debug']:
                    elapsed = timer_fv.get()
                    print("DEBUG: find_valids took " + str(elapsed))
                    print("DEBUG: angle: " + str(angle) + " valid_update: " + str(valid_update) + " valid_count: " + str(valid_count) )
                if valid_update:
                    valid_count += 1
                if n > freqFramesNT:
                    nt_send(camera_table, angle, valid_count, valid_update)
                    n = 0
                else:
                    n += 1
            except:
                print("WARNING: There was an error with find_valids. Continuing.")
                continue
        else:
            print("WARNING: Unable to read frame. Continuing.")
            continue
    else:
        print("ERROR: Capture is not opened. Ending program.")
        sys.exit()


if __name__ == "__main__":
    # execute only if run as a script
    main()
