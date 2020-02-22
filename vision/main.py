import sys
sys.path.append('/usr/local/lib/python3.7/site-packages')
import cv2
import time
import os as OS
import logging
import copy
from util.config import run_config
from util.stopwatch import stopwatch as SW
from networktables import NetworkTables as NT
import find_target as FT
import socket
import numpy as np
from PIL import Image
import threading
from http.server import BaseHTTPRequestHandler,HTTPServer
from socketserver import ThreadingMixIn
from io import StringIO
import time
import redis

logging.basicConfig(level=logging.DEBUG)

# the parameters passed into run_config are the configuration and the filename.
os, camera_location, calibration, freqFramesNT, address = run_config(
    None, None)

capture = None

class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        r = redis.Redis()
        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            last = None
            while True:
                frame = r.get('frame')
                print("camh - length of frame bytes:" + str(len(frame)))
                if frame != last:
                    # print("new? image")
                    maybe = np.frombuffer(frame, dtype=np.uint8) #     .reshape(480, 640, 3)
                    decoded = cv2.imdecode(maybe, 1)
                    print("camh - shape of decoded image: " + str(decoded.shape))
                    jpg = decoded.tostring()
                    self.wfile.write(str.encode("--jpgboundary"))
                    self.send_header('Content-type', 'image/jpeg')
                    self.send_header('Content-length', str(len(jpg)))
                    self.end_headers()
                    self.wfile.write(jpg)
                    last = frame
                # else:
                #     print("same image")
            return
        if self.path.endswith('.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(str.encode('<html><head></head><body>'))
            self.wfile.write(str.encode('<img src="http://raspberrypi.local:1180/cam.mjpg"/>'))
            self.wfile.write(str.encode('</body></html>'))
            return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def main():
    """Main function for the program
    """
    vision_table = nt_init(address)
    cap = cap_init(camera_location)
    desired_rect = create_rect()
    server = ThreadedHTTPServer(('0.0.0.0', 1180), CamHandler)
    print("INFO: streaming server started")
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    r = send_to_redis()
    thread2 = threading.Thread(target=r.process)
    thread2.daemon = True
    thread2.start()
    run(cap, vision_table, calibration, freqFramesNT, desired_rect, r)


class send_to_redis:
    def __init__(self):
        self.r = redis.Redis()
        self.frame = None
        self.stopped = False

    def update(self, img):
        self.frame = img

    def process(self):
        while not self.stopped:
            if self.frame is not None:
                shape = self.frame.shape
                print("send - frame array shape: " + str(shape))
                _, jpeg = cv2.imencode('.JPEG', self.frame)
                h, w = jpeg.shape
                print("send - jpeg size: " + str(h) + " x " + str (w))
                jpg_bytes = jpeg.tobytes()
                # print("length of sent image: " + str(len(jpg_bytes)))
                self.r.set('frame', jpg_bytes)
            self.frame = None


def nt_init(robot_address):
    """Initialize network tables

    Arguments:
        robot_address {str} -- Address for the roborio

    Returns:
        object -- The vision table from the network tables
    """
    bot_address_found = False
    while not bot_address_found:
        try:
            robot_ip = None
            robot_ip = socket.gethostbyname(
                robot_address)  # determine robot IP
            if robot_ip is not None:
                print("INFO: Found robot at " + robot_ip)
                bot_address_found = True
        except socket.gaierror:
            # this will loop until we find the robot
            print("WARNING: Unable to find robot IP Address.")
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


def create_rect():
    """Creates a rectangle and performs appropriate processing to provide a target

    Returns:
        tuple -- the two contours of the rectangle we want to validate targets against
    """
    img = cv2.imread("../images/2020_target.png")
    ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    contour, _ = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contour, 0, (0, 255, 0), 3)
    return contour


def nt_send(vision_table, angle, valid_count, valid_update, heartbeat):
    """Send relevant data to the network table

    Arguments:
        vision_table {object} -- vision network table
        angle {[type]} -- [description]
        valid_count {[type]} -- [description]
        valid_update {[type]} -- [description]
    """
    vision_table.putNumber("Vision.angle", angle)
    vision_table.putBoolean("Vision.locked", valid_update)
    vision_table.putNumber("Vision.count", valid_count)
    vision_table.putNumber("Vision.heartbeat", heartbeat)


def cap_init(camera_location):
    """[summary]

    Arguments:
        camera_location {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    try:
        cap = cv2.VideoCapture(eval(camera_location))
        time.sleep(1)
    except:
        print("Exception on VideoCapture init. Dying")
        sys.exit()
    return cap


def run(cap, vision_table, calibration, freqFramesNT, desired_cnt, redis):
    """[summary]

    Arguments:
        cap {[type]} -- [description]
        vision_table {[type]} -- [description]
        calibration {[type]} -- [description]
        freqFramesNT {[type]} -- [description]
        desired_cnt {[type]} -- [description]
    """
    valid_count = 0
    heartbeat = 0
    n = 0
    x = 0
    recent_vals = []
    while cap.isOpened():
        heartbeat += 1
        x += 1
        ret, frame = cap.read()
        if ret:
            redis.update(frame)
            try:
                if calibration['debug']:
                    timer_fv = SW('FV')
                    timer_fv.start()
                angle, valid_update, crosshair, mask = FT.find_valids(
                    frame, calibration, desired_cnt)
                # Checking for anomalies
                if calibration['debug']:
                    print(recent_vals)
                if len(recent_vals) != 5:
                    average_angle = 0 #  TAKE THIS OUT
                    if angle != 1000:
                        recent_vals.append(angle)
                else:
                    average_angle = sum(recent_vals) / len(recent_vals)
                    recent_vals.pop(0)
                if valid_update:
                    valid_count += 1
                if calibration['debug']:
                    elapsed = timer_fv.get()
                    print("DEBUG: find_valids took " + str(elapsed))
                    print("DEBUG: angle: " + str(average_angle) + " valid_update: " +
                        str(valid_update) + " valid_count: " + str(valid_count))
                if n > freqFramesNT:
                    nt_send(vision_table, average_angle, valid_count,
                            valid_update, heartbeat)
                    n = 0
                else:
                    n += 1
            except Exception as e:
                print("WARNING: Exception: " + str(e))
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
