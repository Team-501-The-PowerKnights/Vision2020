import subprocess
import os
import pytest
from command import run_command

os.chdir("../vision")


def test_centered():
    angle, results = run_command("2020_target.png")
    assert results == 1
    assert angle < 1


def test_top():
    angle, results = run_command("topTest.jpg")
    assert results == 1
    assert angle < 1


def test_bottom():
    angle, results = run_command("bottomTest.jpg")
    assert results == 1
    assert angle < 1
