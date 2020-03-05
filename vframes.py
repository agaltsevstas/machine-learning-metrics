#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Converts video to JPG frames

@author: Maxim
"""
import cv2
import os,sys,inspect
import numpy as np
#currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.join(os.path.dirname(__file__), "../training")
sys.path.insert(0,parentdir) 
import pm_utils as pm

# Expected arguments
expected = ["input video", "skip=0", "start=0[s]", "end=0[s]", "roi=0,0,0,0"]
values = ["", "0", "0", "0", "0,0,0,0"]
description = "Converts one video to another with change of FPS, time period or region of interest"
values = pm.parseArguments(sys.argv, expected, values, __file__, description)

input = values[0]
skip = int(values[1])
start = int(values[2])
end = int(values[3])
x,y,w,h = np.array(values[4].split(",")).astype(np.int)
assert(os.path.exists(input))
assert(skip >= 0)
assert(start >= 0)
assert(end >= start)
assert(x >= 0 and y >= 0 and w >= 0 and h >= 0)

output = input[:-4] + "/"
print("output:", output)
if not os.path.exists(output):
    os.makedirs(output)

cap = cv2.VideoCapture(input)
in_fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
count = -1
while(cap.isOpened()):    
    count += 1
    t = int(1.0 * count / in_fps)
    if end > 0 and t > end:
        break
    ret, frame = cap.read()
    if not ret:
        break
    if t < start:
        continue
    if (skip > 0) and (count % skip != 0):
        continue
    fname = os.path.join(output, str(count) + ".jpg")
    if w*h == 0:
        cv2.imwrite(fname, frame)
    else:
        towrite = frame[y:y+h, x:x+w]
        cv2.imwrite(fname, towrite)
cap.release()

