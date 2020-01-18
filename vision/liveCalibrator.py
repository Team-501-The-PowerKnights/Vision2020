"""
Live calibrator for opencv2 HSV masking / FIRST Robotics
Reads config.ini for previous values to 'get close'
Uses main vision source, the mjpegstreamer onboard

ESC or q to quit
w to write updated calibration to config.ini (along with the rest of the previous config)

CAUTION: this program reads and writes the main vision config.ini
IF IT BREAKS, YOU WILL HAVE A BAD DAY.

author: ionigman@gmail.com

License: Free As In Beer

"""

import cv2
import numpy as np
from util.config import run_config, write_cal


def nothing(x):
    pass


def init_capture(cam):
    try:
        if len(cam) == 1:
            print("INFO: using local camera device")
        cap = cv2.VideoCapture(eval(cam))
        return cap
    except:
        print('capture failed.')


def init_window(calibration):

    hl, sl, vl = calibration['green']['green_lower']
    hh, sh, vh = calibration['green']['green_upper']

    # Create a black image, a window
    cv2.namedWindow('image')

    # create trackbars for color change
    cv2.createTrackbar('H_low', 'image', 0, 255, nothing)
    cv2.createTrackbar('H_high', 'image', 0, 255, nothing)
    cv2.createTrackbar('S_low', 'image', 0, 255, nothing)
    cv2.createTrackbar('S_high', 'image', 0, 255, nothing)
    cv2.createTrackbar('V_low', 'image', 0, 255, nothing)
    cv2.createTrackbar('V_high', 'image', 0, 255, nothing)

    # set trackbars to values in the calibration file so we're close
    cv2.setTrackbarPos('H_low', 'image', hl)
    cv2.setTrackbarPos('S_low', 'image', sl)
    cv2.setTrackbarPos('V_low', 'image', vl)
    cv2.setTrackbarPos('H_high', 'image', hh)
    cv2.setTrackbarPos('S_high', 'image', sh)
    cv2.setTrackbarPos('V_high', 'image', vh)

    # create switch for ON/OFF functionality
    switch = '0 : OFF \n1 : ON'
    cv2.createTrackbar(switch, 'image',0,1,nothing)

    return switch


def main():
    _, cam, calibration, _, _ = run_config(None, 'config.ini')
    cap = init_capture(cam)
    switch = init_window(calibration)
    run(cap, switch, calibration)


def run(cap, switch, calibration):
    while True:
        img = None
        try:
            if cap.isOpened():
                _, img = cap.read()
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            else:
                print('cannot open capture')
        except:
            print('capture read exception')

        hl = cv2.getTrackbarPos('H_low', 'image')
        hh = cv2.getTrackbarPos('H_high', 'image')
        sl = cv2.getTrackbarPos('S_low', 'image')
        sh = cv2.getTrackbarPos('S_high', 'image')
        vl = cv2.getTrackbarPos('V_low', 'image')
        vh = cv2.getTrackbarPos('V_high', 'image')
        lower_bound = np.array([hl, sl, vl])
        upper_bound = np.array([hh, sh, vh])

        s = cv2.getTrackbarPos(switch, 'image')
        if s == 0:
            pass
        else:
            img = cv2.inRange(hsv, lower_bound, upper_bound)
        cv2.imshow('image', img)
        k = cv2.waitKey(15) & 0xFF
        if k == 27 or k == 113: # 'q' or ESC pressed
            break
        if k == 119: # 'w' pressed
            calibration['green']['green_lower'] = [str(hl), str(sl), str(vl)]
            calibration['green']['green_upper'] = [str(hh), str(sh), str(vh)]
            write_cal(calibration)
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # execute only if run as a script
    main()