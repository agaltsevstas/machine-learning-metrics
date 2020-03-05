#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Adds the second PMXML to the first one, saves to output

@author: Maxim Mukhortov
"""

import cv2
import sys
import os
import numpy as np
import pm_utils as pm

# Expected arguments
expected = ["first xml path", "second xml path", "output xml path"]
values = np.array(["", "", "-"])
description = "Adds the second PMXML to the first one, saves to output"
values = pm.parseArguments(sys.argv, expected, values, __file__, description)

# Validation
xmlfiles = [values[0], values[1]]
workdir = os.path.dirname(values[0])
output = values[2]
assert(os.path.exists(xmlfiles[0]))
assert(os.path.exists(xmlfiles[1]))
if len(output) == 1:
    output = os.path.join(workdir, "add_%s_%s.xml"%tuple(os.path.basename(fpath)[:-4] for fpath in xmlfiles))

# Function
files_objects = [pm.readXml(fpath) for fpath in xmlfiles]

res_objects = dict()
for file_list in files_objects:
    for filepath in file_list.keys():
        fname = os.path.basename(filepath)
        if not fname in res_objects:
            res_objects[fname] = file_list[filepath]

pm.writeXml(res_objects, output)
print("Saved to %s"%output)