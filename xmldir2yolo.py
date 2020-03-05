#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Converts XMLPM (xml pattern marker) list to YOLO txt files

@author: maxim
"""

import sys
import os
import numpy as np
import pm_utils as pm
import subprocess, sys

# Expected arguments
expected = ["root catalog path", "classes map file"]
values = np.array(["", ""])
description = "Converts catalog with subcatalogs containing XML lists to YOLO TXT annotations"
values = pm.parseArguments(sys.argv, expected, values, __file__, description)

# Catalogs and files
root = values[0]
classes_file = values[1]

# Check parameters   
assert(os.path.exists(root))
assert(os.path.exists(classes_file))
catalogs = [os.path.join(root, fname) for fname in os.listdir(root) if os.path.isdir(os.path.join(root, fname))]
assert(len(catalogs) > 0)
#print(catalogs)

cmd = os.path.join(os.path.dirname(os.path.realpath(__file__)), "xml2yolo.py");
print("Command:", cmd)

# Find XML lists
for catalog in catalogs:
    print(catalog)
    xmlfiles = [os.path.join(catalog, fname) for fname in os.listdir(catalog) if (len(fname)>4) and (fname[-3:] == "xml")]
    if len(xmlfiles) == 0:
        print("WARNING: no XML files")
        continue
    elif len(xmlfiles) > 1:
        print("WARNING: many XML files, takes first")
    xmlpath = xmlfiles[0]
    process = subprocess.Popen([cmd, xmlpath, classes_file], stdout=subprocess.PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()

    

