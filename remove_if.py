#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Puts fimages, containing specified class objects, to catalog 'removed'

@author: Maxim Mukhortov
"""

import cv2
import sys
import os
import numpy as np
import pm_utils as pm
import shutil

# Expected arguments
expected = ["xml path", "classname", "output"]
values = np.array(["", "", "-"])
description = "Puts fimages, containing specified class objects, to catalog 'removed'"
values = pm.parseArguments(sys.argv, expected, values, __file__, description)

# Validation
xmlpath = values[0]
workdir = os.path.dirname(xmlpath)
classname = values[1]
output = values[2]
assert(os.path.exists(xmlpath))
if len(output) == 1:
    output = os.path.join(workdir, "removed_%s"%os.path.basename(xmlpath))

# 'remove' catalog
remove_dir = os.path.join(workdir, 'removed')
if not os.path.exists(remove_dir):
	os.mkdir(remove_dir)

# Function
files_objects = pm.readXml(xmlpath)

res_objects = dict()
for filepath in files_objects.keys():
    fname = os.path.basename(filepath)
    do_remove = False
    for obj in files_objects[filepath]:
    	if obj[4] == classname:
    		do_remove = True
    		break
    if do_remove:
    	shutil.move(os.path.join(workdir, fname), os.path.join(remove_dir, fname))
    	print("'removed'%s"%fname)
    else:
    	res_objects[fname] = files_objects[filepath]

pm.writeXml(res_objects, output)
print("Saved to %s"%output)