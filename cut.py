#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Cuts images of objects of certain class

@author: Maxim Mukhortov
"""

import cv2
import sys
import os
import numpy as np
import pm_utils as pm

# Expected arguments
expected = ["xml file path", "images path", "class name", "output catalog"]
values = np.array(["", "", "", ""])
description = "Cuts images of objects of certain class"
values = pm.parseArguments(sys.argv, expected, values, __file__, description)

# Validation
xmlpath = values[0]
workdir = values[1]
outdir = values[3]
classname = values[2]
assert(os.path.exists(xmlpath))
if not os.path.exists(outdir):
    os.mkdir(outdir)

# Function
files_objects = pm.readXml(xmlpath)
i = 0
for fname in files_objects.keys():
    objects = files_objects[fname]
    print(1.0 * i / len(files_objects), "\t", fname, "\t", len(objects))
    if len(objects) == 0:
        continue
    fpath = os.path.join(workdir, fname)    
    image = cv2.imread(fpath, cv2.IMREAD_COLOR)
    for o in files_objects[fname]:
        x,y,w,h,c = o
        outpath = os.path.join(outdir, fname[:-4] + "_%s_%d_%d.png"%(c, x, y))
        if c == classname:
            img_ob = image[y:y+h, x:x+w]
            cv2.imwrite(outpath, img_ob)

