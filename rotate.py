#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Rotates all images over 90 degrees with objects from PMXML list, adds rotated images to catalog

@author: Maxim Mukhortov
"""

import cv2
import sys
import os
import numpy as np
import pm_utils as pm
import shutil
import copy

ADD_UNDIST_PREFIX = True

# Expected arguments
expected = ["xml path", "output", "image path"]
values = np.array(["", "-", "-"])
description = "Rotates all images over 90 degrees with objects from PMXML list, adds rotated images to catalog"
values = pm.parseArguments(sys.argv, expected, values, __file__, description)

# Validation
xmlpath = values[0]
workdir = os.path.dirname(xmlpath)
output = values[1]
assert(os.path.exists(xmlpath))
if len(output) == 1:
    output = os.path.join(workdir, "rotated_%s"%os.path.basename(xmlpath))

image_path = values[2]
assert(os.path.exists(image_path))

# Rotates image and objects over 90deg
def rotate90(image, objects):
    rows = np.shape(image)[0]
    res_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    res_objects = []
    for obj in objects:
        x,y,w,h,c = obj
        x1 = rows - y - h
        y1 = x
        w1 = h
        h1 = w
        res_objects.append([x1, y1, w1, h1, c])
    return res_image, res_objects

# Function
files_objects = pm.readXml(xmlpath)

res_objects = dict()
for filepath in files_objects.keys():
    fname = os.path.basename(filepath)
    if ADD_UNDIST_PREFIX:
        if fname[-6:-4] != "_u":
            fname = fname[:-4] + "_u" + fname[-4:]    
    print(fname)
    inpath = os.path.join(image_path, fname)
    image = cv2.imread(inpath, cv2.IMREAD_COLOR)
    res_objects[fname] = files_objects[filepath]
    objects = copy.deepcopy(res_objects[fname])
    # Rotate
    angles = [90, 180, 270]
    for deg in angles:
        outname = fname[:-4] + "deg%i"%deg + fname[-4:]
        outpath = os.path.join(image_path, outname)   
        image, objects = rotate90(image, objects) 
        cv2.imwrite(outpath, image)
        res_objects[outname] = copy.deepcopy(objects)
    #break

pm.writeXml(res_objects, output)
print("Saved to %s"%output)
