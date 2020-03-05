#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Prepares trin.txt and test.txt from divided data in image catalog and xml file

@author: maxim
"""

import sys
import os
from sklearn.model_selection import train_test_split
import numpy as np
import pm_utils as pm
import random

# Expected arguments
expected = ["input catalog (contains img-txt or subcatalogs)", "output catalog", "test part = 0.2"]
values = np.array(["", "", "0.3"])
description = "Divides images-txts in yolo format into train/valid"
values = pm.parseArguments(sys.argv, expected, values, __file__, description)

input_catalog = values[0]
output_catalog = values[1]
Pvalid = float(values[2])

# Macros for indexing
TRAIN = 0
VALID = 1
NAMES = ["train", "valid"]

# Catalogs and files
print(input_catalog)
print(output_catalog)
print("Pvalid", Pvalid)

# Check parameters   
assert(os.path.exists(input_catalog))
assert(os.path.exists(output_catalog))

outfiles = [os.path.join(output_catalog, NAMES[i]) + ".txt" for i in range(2)]
print(outfiles)
      
# Get files lists
extensions = ["txt"]
fileslist = [os.path.join(input_catalog, fname) for fname in os.listdir(input_catalog) 
                        if (len(fname)>4) and (fname[-3:] in extensions) and os.path.isfile(os.path.join(input_catalog, fname))]
subdirs = [os.path.join(input_catalog, fname) for fname in os.listdir(input_catalog) if os.path.isdir(os.path.join(input_catalog, fname))]
if len(subdirs) > 0:
    print(subdirs)
    for subdir in subdirs:
        subfiles = [os.path.join(subdir, fname) for fname in os.listdir(subdir) 
                        if (len(fname)>4) and (fname[-3:] in extensions) and os.path.isfile(os.path.join(subdir, fname))]
        fileslist = fileslist + subfiles
print('files', len(fileslist))

outstreams = [open(outfiles[i], 'w') for i in range(2)]
#relpath = os.path.relpath(input_catalog, output_catalog)
#relpath = input_catalog

for fpath in fileslist:
    fname = os.path.basename(fpath)
    relpath = os.path.dirname(fpath)
    p = random.random()
    index = TRAIN
    if p < Pvalid:
        index = VALID
    fpath_jpg = os.path.join(relpath, fname[:-3] + "jpg")
    fpath_png = os.path.join(relpath, fname[:-3] + "png")
    if os.path.exists(fpath_jpg):
    	outstreams[index].write(fpath_jpg + "\n")  
    elif os.path.exists(fpath_png):
    	outstreams[index].write(fpath_png + "\n")  
    #break    

for i in range(2):
    outstreams[i].close()
