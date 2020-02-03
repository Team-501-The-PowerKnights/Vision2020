import os
import subprocess


def run_command(img_name):
    # Writing to image path file:
    os.system("rm -f imgName.txt")
    os.system("touch imgName.txt")
    os.system("touch imgName.txt")
    with open("imgName.txt", "w") as imgNameFile:
        imgNameFile.write(img_name)
    # Running program:
    command_output = subprocess.run(
        ["python3", "../vision/main.py"], stdout=subprocess.PIPE).stdout.decode('utf-8').split("\n")
    print("command_output:", command_output)
    angle = float(command_output[-2].split(" ")[2])
    valid_count = int(command_output[-2].split(" ")[-1])
    return angle, valid_count
