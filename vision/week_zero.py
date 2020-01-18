from util.stopwatch import stopwatch as SW
import cv2
import sys
import time
from networktables import NetworkTables as NT
import socket

# random change
def main():
    global timer
    timer = SW('timer')
    timer.start()
    nt = init_nt()
    cam = init_cv()
    loop(cam, nt)


def init_nt():
    robot = 'roborio-501-frc.local'  # set robot name
    robot_ip = socket.gethostbyname(robot)  # determine robot IP
    nt_init = False

    while not nt_init:
        try:
            NT.initialize(server=robot_ip)  # initialize client
        except:
            continue
        try:
            vision_table = NT.getTable('SmartDashboard')
        except:
            NT.stop()
            NT.destroy()
            continue
        vision_table.putBoolean('Vision.pullback', True)
        pullback = vision_table.getBoolean('Vision.pullback', None)
        if pullback:
            nt_init = True
        else:
            continue
    else:
        return vision_table


def init_cv():
    try:
        cam = cv2.VideoCapture('http://tinkerboard.local:1180/?action=stream?dummy=param.mjpg')
        time.sleep(1)
        # print('camera init.')
    except:
        print("Exception on VideoCapture init. Dying")
        sys.exit()
    return cam


def loop(camera, network_table):
    while camera.isOpened():
        pose = network_table.getBoolean('Robot.strikingAPose', None)
        arm = network_table.getBoolean('Arm.inMotion', None)
        wrist = network_table.getBoolean('Wrist.inMotion', None)
        elbow = network_table.getBoolean('Elbow.inMotion', None)
        if pose or arm or wrist or elbow:
            ret, frame = camera.read()
            if ret:
                current_time = timer.get()
                formatted_time = "%.3f" % (current_time)
                filename = "/home/linaro/match_images/live_match"+formatted_time+".jpg"
                cv2.imwrite(filename, frame)
                time.sleep(0.133)
            else:
                time.sleep(0.133)
                continue
        else:
            time.sleep(0.133)


if __name__ == "__main__":
    main()
