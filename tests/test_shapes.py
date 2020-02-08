import subprocess
import os
from command import run_command

os.chdir("../vision")


def test_leftSquare():
    angle, results = run_command("leftSquareRightTest.jpg")
    assert results == 1
    assert angle < 14


def test_leftTriangle():
    angle, results = run_command("leftTriangleRightTest.jpg")
    assert results == 1
    assert angle < 14


def test_rightSquare():
    angle, results = run_command("rightSquareLeftTest.jpg")
    assert results == 1
    assert angle < 14


def test_leftSquare():
    angle, results = run_command("leftSquareRightTest.jpg")
    assert results == 1
    assert angle < 14
