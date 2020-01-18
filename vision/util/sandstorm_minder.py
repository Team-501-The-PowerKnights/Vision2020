from networktables import NetworkTables as NT
import socket
import subprocess

def main():
    network_table = nt_init("roborio-501-frc.local")
    sandstorm(network_table)

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
                bot_address_found = True
        except socket.gaierror:
            print("WARNING: Unable to find robot IP Address.")
            continue

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
        vision_table.putBoolean('connected', True)
        pullback = vision_table.getBoolean('connected', None)
        if pullback:
            nt_init = True
        else:
            continue
    else:
        return vision_table


def sandstorm(vision_table):
    vision_on = False
    while not vision_on:
        is_sandstorm = vision_table.getBoolean('Vision.isSandstorm')
        if not is_sandstorm:
            break

    subprocess.call(['./camera_teleop.sh'])

if __name__ == "__main__":
    # execute only if run as a script
    main()
