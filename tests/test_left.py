import subprocess
import os
from command import run_command

os.chdir("../vision")


def test_left():
    angle, results = run_command("leftTest.jpg")
    assert results == 1
    assert angle < 14


def test_leftTop():
    angle, results = run_command("topLeftTest.jpg")
    assert results == 1
    assert angle < 14


def test_leftBottom():
    angle, results = run_command("bottomLeftTest.jpg")
    assert results == 1
    assert angle < 14
