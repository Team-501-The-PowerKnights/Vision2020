from networktables import NetworkTables as NT
import socket
from collections import namedtuple
import time

"""
Telemetry Push Subsystem 
****
ONLY WORKS ON LINUX
****
Provides the following information to the Driver Station:
- SOC Temperature (thermal_zone0)
- CPU Frequency
- Free Memory
"""


sleep_time = 0.200  # time to wait between sending updates


def main():
    table = telemetry_init()  # looks up robot address and returns networktable
    telemetry_run(table)  # sends telemetry


def telemetry_init():
    robot = 'roborio-501-frc.local'  # set robot name

    bot_address_found = False
    while not bot_address_found:
        try:
            robot_ip = None
            robot_ip = socket.gethostbyname(robot)  # determine robot IP
            if robot_ip is not None:
                bot_address_found = True
        except socket.gaierror:
            print("Unable to find robot IP Address.")
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


def telemetry_run(vision_table):
    while True:
        try:
            with open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq') as f:  # read CPU frequency
                cpu_freq = int(f.read())
            f.closed
            if cpu_freq:
                MHz = int(cpu_freq / 1000.0)
            else:
                MHz = 0
            clock_speed = str(MHz) + ' MHz'
        except:
            print('ERROR: Unable to process clockspeed information')
            continue

        try:
            with open('/sys/class/thermal/thermal_zone0/temp') as f:  # read SOC temperature
                soc_temp = int(f.read())
            f.closed
            if soc_temp:
                soc_temp = str(int(soc_temp / 1000)) + ' C'
            else:
                soc_temp = '0 C'
        except:
            print('ERROR: Unable to process temperature information')
            continue

        MemInfoEntry = namedtuple('MemInfoEntry', ['value', 'unit'])  # gets memory information
        mem_info = {}
        try:
            with open('/proc/meminfo') as file:
                for line in file:
                    key, value, *unit = line.strip().split()
                    mem_info[key.rstrip(':')] = MemInfoEntry(value, unit)
            file.closed
            free_memory = str(int(int(mem_info['MemFree'][0]) / 1000 )) + ' MB'
        except:
            print('ERROR: Unable to process memory information')
            continue

        try:
            vision_table.putString('RPI/clock_speed', clock_speed)
            vision_table.putString('RPI/soc_temp', soc_temp)
            vision_table.putString('RPI/free_memory', free_memory)
        except:
            print('ERROR: Problem sending networktables data (type error? see above)')
        time.sleep(sleep_time)


if __name__ == "__main__":
    # execute only if run as a script
    main()
