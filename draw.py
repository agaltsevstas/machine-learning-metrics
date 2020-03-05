#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Draws objects on image, puts to 'draw' catalog

@author: Maxim Mukhortov
"""

import cv2
import sys
import os
import numpy as np
import pm_utils as pm
import shutil

# Expected arguments
expected = ["xml path"]
values = np.array([""])
description = "Draws objects on image, puts to 'draw' catalog"
values = pm.parseArguments(sys.argv, expected, values, __file__, description)

# Validation
xmlpath = values[0]
workdir = os.path.dirname(xmlpath)
assert(os.path.exists(xmlpath))

# 'remove' catalog
draw_dir = os.path.join(workdir, 'draw')
if not os.path.exists(draw_dir):
	os.mkdir(draw_dir)

# Function
files_objects = pm.readXml(xmlpath)

res_objects = dict()
for filepath in files_objects.keys():
    fname = os.path.basename(filepath)
    inpath = os.path.join(workdir, fname)
    outpath = os.path.join(draw_dir, fname)
    color = [0, 255, 0]
    image = cv2.imread(inpath, cv2.IMREAD_COLOR)
    for obj in files_objects[filepath]:
        x,y,w,h,c = obj
        image = cv2.rectangle(image, (x,y), (x+w, y+h), color, 2)
    cv2.imwrite(outpath, image)

