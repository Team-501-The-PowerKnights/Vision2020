import cv2
import numpy as np
import image_calculations as IC
from heapq import nlargest
import manipulate_image as MI


def isValidShape(contour, rect_cnt, rect_cnt2):
    """
    Use cv2.matchShapes to see if the contour is close enough to the shape we are looking for
    :param contour: contour of potential target being analyzed
    :param rect_cnt: contour of what the perfect target should be
    :return: boolean, True if the shape match is within the allowable threshold, False otherwise
    """
    match_threshold = 0.35

    match_quality1 = cv2.matchShapes(rect_cnt, contour, 2, 0)
    match_quality2 = cv2.matchShapes(rect_cnt2, contour, 2, 0)
    if match_quality1 < match_threshold or match_quality2 < match_threshold:
        return True
    else:
        return False


def sortArray(sorted_indices, array):
    """
    Sort an array according to the provided indices
    :param sorted_indices: the indices provided by argsort
    :param array: the array to sort
    :return: a sortedf array
    """
    sorted = []
    for index in sorted_indices:
        sorted.append(array[index])
    return sorted


def find_valid_target(mask, desired_cnt):
    """

    :param image: frame to be analyzed
    :param mask: mask of thresholded hsv image
    :param rect_cnt1: contour of perfect target rectangle
    :param rect_cnt2: contour of the other perfect target rectangle
    :return: valid: boolean, True if valid target, False otherwise
            cnt: list where first entry is the contour of target 1 and second entry is contour of target 2
            cx: list of the center of mass for x of the two contours
            cy: list of the center of mass for y of the two contours
    """
    # This needs to be rewritten to accept only one contour
    pass
