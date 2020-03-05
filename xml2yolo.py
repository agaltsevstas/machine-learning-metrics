#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Converts XMLPM (xml pattern marker) list to YOLO txt files

@author: maxim
"""

import cv2
import sys
import os
import numpy as np
import pm_utils as pm
import xml.etree.ElementTree as ET

# Expected arguments
expected = ["xml file path", "classes map file"]
values = np.array(["", ""])
description = "Converts XML PM list to YOLO txt files"
values = pm.parseArguments(sys.argv, expected, values, __file__, description)

# Catalogs and files
xmlfile = values[0]
xmldir = os.path.dirname(xmlfile)
classes_file = values[1]
print(xmlfile)
print(xmldir)

# Check parameters   
assert(os.path.exists(xmlfile))
assert(os.path.exists(classes_file))
      
# Get files lists
extensions = ["jpg", "png"]
filelist = [fname for fname in os.listdir(xmldir) if (len(fname)>4) and (fname[-3:] in extensions)]
print('Files count', len(filelist))

# Parse XML
tree = ET.parse(xmlfile)
root = tree.getroot()
assert(root.tag == "list")

# Open output files 
classes = dict()
sep = ':'
file = open(classes_file, 'r')
lines = file.readlines()
i = 0
for line in lines:    
    string = line.strip()
    if len(string) == 0:
        continue
    assert(not ' ' in string)
    if sep in string:
        parts = string.split(sep)
        classes[parts[0]] = int(parts[1])
    else:
        classes[string] = i
    i += 1
file.close()
print(classes)
#exit(0)

# Files loop
for filenode in root:
    if filenode.tag != "file":
        continue
    # Objects getting loop
    objects = []
    for objnode in filenode:   
        if objnode.tag != "object":
            continue
        clsname = objnode.attrib["className"]
        if not clsname in classes:
            continue
        x = int(objnode.attrib["x"])
        y = int(objnode.attrib["y"])
        width = int(objnode.attrib["width"])
        height = int(objnode.attrib["height"])
        cls = classes[clsname]
        objects.append([x, y, width, height, cls])
    # Find image and create text file near it
    relpath = filenode.attrib["path"].replace('\\', '/')
    imname = os.path.basename(relpath)
    print(imname)
    if imname in filelist:
        txtpath = os.path.join(xmldir, relpath[:-3] + "txt")
        impath = os.path.join(xmldir, relpath)
        if not os.path.exists(impath):
            continue
        img = cv2.imread(impath, cv2.IMREAD_COLOR)
        rows, cols = np.shape(img)[0:2]
        imstream = open(txtpath, 'w')
        # Collecting lines: class x y w h
        for obj in objects:
            line = str(obj[4])
            # mirror coordinates if need
            w = float(obj[2]) / cols
            h = float(obj[3]) / rows
            x = float(obj[0]) / cols + 0.5 * w
            y = float(obj[1]) / rows + 0.5 * h
            if "mir" in imname:
                x = 1.0 - x
                y = 1.0 - y  
            newobj = [x, y, w, h]  
            line += ' %.3f' % x + ' %.3f' % y + ' %.3f' % w + ' %.3f' % h
            line += "\n"
            imstream.write(line)
        imstream.close()
        #break
    #break
    

