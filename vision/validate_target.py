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


def find_valid_target(mask, rect_cnt1, rect_cnt2):
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
    # initialize variables
    numContours = 10
    # find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # take 10 longest contours
    biggestContours = nlargest(numContours, contours, key=len)
    # get area of each contour
    areas = []
    goodContours = []
    if len(biggestContours) > 1:
        for cnt in biggestContours:
            areas.append(cv2.contourArea(cnt))
        sorted_indices = np.argsort(areas)
        max_index = np.where(sorted_indices == len(sorted_indices) - 1)[0][0]
        second_index = np.where(sorted_indices == len(sorted_indices) - 2)[0][0]
        biggestContours = [biggestContours[max_index], biggestContours[second_index]]
        # check validity of contours by shape match
        for contour in biggestContours:
            if isValidShape(contour, rect_cnt1, rect_cnt2):
                goodContours.append(contour)
        # get the center of mass for each valid contour
        xCOM = []
        yCOM = []
        for contour in goodContours:
            cx, cy = IC.findCenter(contour)
            xCOM.append(cx)
            yCOM.append(cy)
    if len(goodContours) < 2:
        cnt = [0, 0]
        valid = False
        cx = [0, 0]
        cy = [0, 0]
    else:
        cnt = goodContours
        valid = True
        cx = xCOM
        cy = yCOM
    return valid, cnt, cx, cy
