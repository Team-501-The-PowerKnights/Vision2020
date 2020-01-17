import cv2
from datetime import datetime
import numpy as np
load_start = datetime.now()
img: cv2.UMat = cv2.imread('../images/2020_target.png')
load_end = datetime.now()
ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
thresh_end = datetime.now()
cv2.imwrite('../images/threshold_raw.png', thresh)
color_start = datetime.now()
thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
color_end = datetime.now()
cv2.imwrite('../images/threshold_colorized.png', thresh)
cont_start = datetime.now()
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cont_end = datetime.now()
# print(contours[0])
# print(len(contours[0]))
output = cv2.drawContours(img, contours, 0, (0, 255, 0), 3)
cv2.imwrite('../images/contours.png', output)

loadtime = load_end - load_start
threshtime = thresh_end - load_end
colortime = color_end - color_start
conttime = cont_end - cont_start

print("load: " + str(loadtime))
print("threshold: " + str(threshtime))
print("colorize: " + str(colortime))
print("find contours: " + str(conttime))

np_arr = np.array(contours[0])
# string_cont = str(contours)
# print(string_cont)
print(np_arr.shape)
