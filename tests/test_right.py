import subprocess
import os
from command import run_command

os.chdir("../vision")


def test_left():
    angle, results = run_command("rightTest.jpg")
    assert results == 1
    assert angle > -13


def test_leftTop():
    angle, results = run_command("topRightTest.jpg")
    assert results == 1
    assert angle > -13


def test_leftBottom():
    angle, results = run_command("bottomRightTest.jpg")
    assert results == 1
    assert angle > -13
