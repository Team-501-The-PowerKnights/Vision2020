import cv2
import numpy as np
import image_calculations as IC
from heapq import nlargest
import manipulate_image as MI


def isValidShape(contour, desired_cnt):
    """[summary]

    Arguments:
        contour {[type]} -- [description]
        desired_cnt {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    match_threshold = 2.8
    match_quality1 = cv2.matchShapes(
        desired_cnt[0], contour[0], 1, 0.0)
    match_quality2 = cv2.matchShapes(
        desired_cnt[0], contour[0], 2, 0.0)
    match_quality3 = cv2.matchShapes(
        desired_cnt[0], contour[0], 3, 0.0)
    matches = [match_quality1, match_quality2, match_quality3]
    match_quality = min(matches)
    match_index = matches.index(min(matches))
    print("match index: " + str(match_index))
    if match_quality < match_threshold:
        return True
    else:
        return False


def sortArray(sorted_indices, array):
    """[summary]

    Arguments:
        sorted_indices {[type]} -- [description]
        array {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    sorted = []
    for index in sorted_indices:
        sorted.append(array[index])
    return sorted


def find_valid_target(mask, desired_cnt):
    """[summary]

    Arguments:
        mask {[type]} -- [description]
        desired_cnt {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    # initialize variables
    numContours = 10
    # find contours
    contours, _ = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # get area of each contour
    biggestContours = sorted(contours, key=len, reverse=True)
    areas = []
    goodContours = []
    if len(biggestContours) > 0:
        for cnt in biggestContours:
            areas.append(cv2.contourArea(cnt))
        sorted_indices = np.argsort(areas)
        max_index = np.where(sorted_indices == len(sorted_indices) - 1)[0][0]
        if len(sorted_indices) > 1:
            second_index = np.where(
                sorted_indices == len(sorted_indices) - 2)[0][0]
        else:
            second_index = max_index
        biggestContours = [[biggestContours[max_index]],
                           [biggestContours[second_index]]]
        # check validity of contours by shape match
        for contour in biggestContours:
            if isValidShape(contour, desired_cnt):
                goodContours.append(contour)
        # get the center of mass for each valid contour
    if len(goodContours) == 0:
        cnt = [0]
        valid = False
    else:
        cnt = goodContours[0]
        valid = True
    return valid, cnt
