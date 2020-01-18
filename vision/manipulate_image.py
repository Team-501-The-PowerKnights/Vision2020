"""
Created on Tues Feb 19 08:40:34 2019

@author: Matt-Gleich & dithier

Other important info:
You need to change the camera resolution from 320x240 to you camera's res
"""
import cv2
import numpy as np


def erodeAndDilate(img):
    """
    Erodes and then dilates the mask of the image
    :param img: the image frame mask being analyzed
    :return: and eroded and dilated image
    """
    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(img, kernel, iterations=1)
    erosion_and_dilation = cv2.dilate(erosion, kernel, iterations=1)
    return erosion_and_dilation


def drawLine2Target(img, cx, cy):
    """
    Draws a line from the center of the camera point of view to the center of the target
    :param image: the original frame
    :param cx: x coordinate of target center
    :param cy: y coordinate of target center
    :return: image with a line drawn to target
    """
    dimensions = img.shape
    centery = int(dimensions[0] / 2)
    centerx = int(dimensions[1] / 2)
    img_line = cv2.line(img, (centery, centerx), (cx, cy), (255, 0, 0), 2)
    return img_line

def drawCrossHairs(img):
    """
    Draws cross-hairs in image donating the center of the camera view
    :param img: the image being analyzed
    :return: an image with cross-hairs drawn
    """
    dimensions = img.shape
    centery = int(dimensions[0] / 2)
    print(centery)
    centerx = int(dimensions[1] / 2)
    print(centerx)
    centerx10 = centerx + 10
    centerx30 = centerx + 30
    centerxmin10 = centerx - 10
    centerxmin30 = centerx - 30
    centery10 = centery + 10
    centery30 = centery + 30
    centerymin10 = centery - 10
    centerymin30 = centery - 30
    red = (0, 0, 255)
    top_hair = cv2.line(img, (centerx, centerymin10), (centerx, centerymin30), red, 2)
    bottom_hair = cv2.line(top_hair, (centerx, centery10), (centerx, centery30), red, 2)
    left_hair = cv2.line(bottom_hair, (centerxmin10, centery), (centerxmin30, centery), red, 2)
    crosshairs = cv2.line(left_hair, (centerx10, centery), (centerx30, centery), red, 2)
    return crosshairs
