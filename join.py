#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Concatenates

@author: Maxim Mukhortov
"""

import cv2
import sys
import os
import numpy as np
import pm_utils as pm

# Expected arguments
expected = ["first xml path", "second xml path", "operation=[or/and/all/not]"]
values = np.array(["", "", "or"])
description = "Concatinates two XML lists from same catalog and image set"
values = pm.parseArguments(sys.argv, expected, values, __file__, description)

# Validation
xmlfiles = [values[0], values[1]]
workdir = os.path.dirname(values[0])
operation = values[2]
assert(os.path.exists(xmlfiles[0]))
assert(os.path.exists(xmlfiles[1]))
assert(operation in ['or', 'and', 'all', 'not'])
# assert(workdir == os.path.dirname(values[1]))

# Function
files_objects = [pm.readXml(fpath) for fpath in xmlfiles]

res_objects = dict()
for file1 in files_objects[0].keys():
    for file2 in files_objects[1].keys():   
        print(file1)
        print(file2)     
        if os.path.basename(file1) == os.path.basename(file2):
            print(file1, file2)
            o1 = files_objects[0][file1]
            o2 = files_objects[1][file2]
            # Exclude same objects in o1/o2
            res_o = []
            for a in o1 + o2:
                found = False
                for b in res_o:
                    if pm.same(a, b):
                        found = True
                        break
                if not found:
                    res_o.append(a)
            if operation == 'and' and len(o1)>0 and len(o2)>0:
                res_objects[file1] = res_o
            elif operation == 'or' and (len(o1)>0 or len(o2)>0):
                res_objects[file1] = res_o
            elif operation == 'not' and len(o1) == 0 and len(o2) == 0:
                res_objects[file1] = []
            elif operation == 'all':
                res_objects[file1] = res_o
            break

pm.writeXml(res_objects, os.path.join(workdir, 'out_' + operation + ".xml"))
