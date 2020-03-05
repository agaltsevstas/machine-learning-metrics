#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Pattern Marker XML utils

@author: Maxim Mukhortov
"""

import os
import xml.etree.ElementTree as ET
import numpy as np

# Returns map filename-obj_list[x,y,w,h,c]
# naming = 'absolute', 'relative', 'basename'
def readXml(xmlpath, naming="basename"):
    result = dict()
    # Parse XML
    tree = ET.parse(xmlpath)
    root = tree.getroot()
    assert(root.tag == "list")
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
            x = int(objnode.attrib["x"])
            y = int(objnode.attrib["y"])
            width = int(objnode.attrib["width"])
            height = int(objnode.attrib["height"])
            cls = clsname
            objects.append([x, y, width, height, cls])
        # Find image and create text file near it
        #relpath = os.path.relpath(filenode.attrib["path"].replace('\\', '/'), os.path.dirname(xmlpath))
        #relpath = filenode.attrib["path"].replace('\\', '/')
        path = filenode.attrib["path"].replace('\\', '/')
        if naming == "basename":
            path = os.path.basename(filenode.attrib["path"])
        elif naming == "absolute":
            path = os.path.abspath(os.path.join(os.path.dirname(xmlpath), path))
        elif "/" in path:
            path = os.path.relpath(filenode.attrib["path"].replace('\\', '/'), os.path.dirname(xmlpath))
        result[path] = objects
    return result
        #break
    #break

# Xml file with new lines
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

# Writes objects map{filename:objects[]} to filepath xml
def writeXml(objects, filepath, list_viewed=None):
    root = ET.Element("list")
    for fname in objects.keys():
        filetag = ET.SubElement(root, "file")
        filetag.set("path", fname)
        if list_viewed is not None and fname in list_viewed:
            filetag.set("viewed", "1")
        for obj in objects[fname]:
            objtag = ET.SubElement(filetag, "object")            
            objtag.set('className', obj[4])
            objtag.set('x', str(obj[0]))
            objtag.set('y', str(obj[1]))
            objtag.set('width', str(obj[2]))
            objtag.set('height', str(obj[3]))
    tree = ET.ElementTree(root)
    root = indent(root)    
    tree.write(filepath)

def union(a,b):
    x = min(a[0], b[0])
    y = min(a[1], b[1])
    w = max(a[0]+a[2], b[0]+b[2]) - x
    h = max(a[1]+a[3], b[1]+b[3]) - y
    return (x, y, w, h)

def intersection(a,b):
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    w = min(a[0]+a[2], b[0]+b[2]) - x
    h = min(a[1]+a[3], b[1]+b[3]) - y
    if w<0 or h<0: return (0,0,0,0) 
    return (x, y, w, h)

def same(o1, o2, T=0.7):
    if o1[4] != o2[4]:
        return False
    I = intersection(o1, o2)
    U = union(o1, o2)
    Ai = I[2] * I[3]
    Au = U[2] * U[3]
    if Au * Ai == 0:
        return False
    if 1.0 * Ai / Au < T:
        return False
    return True

# Parses command line arguments, returns values
def parseArguments(sysargv, expected, values, cmdname, description=""):
    values = np.array(values)
    assert(len(values) == len(expected))
    help = description + "\nUsage:\n\t" + cmdname + " " + str([name for name in expected])[1:-1].replace(', ', ' ')
    # Parsing arguments
    argv = sysargv[1:]
    newvalues = ["" for i in range(len(expected))]
    if len(argv) < len(values[values == ""]):
        print(help)
        exit(-1)
    else:
        for i in range(len(expected)):
            if i < len(argv):
                newvalues[i] = argv[i]
            else:
                newvalues[i] = values[i]
            print(expected[i] + ": " + newvalues[i])
    return newvalues

# Unit test
if __name__ == '__main__':
    catalog = "./test/"
    # Xml file info
    xmlname = "input.xml"
    nfiles = 4
    objects_count = {"./0.png":0, "./1.png":5, "./2.png":4, "./3.png":5}
    input = os.path.join(catalog, xmlname)
    output = os.path.join(catalog, "out_" + xmlname)
    # Objects read, check, write, read-check
    print("TEST: xmlRead()")
    files_objects = readXml(input)    
    assert(len(files_objects) == nfiles)
    i = 0
    for f in files_objects.keys():
        assert(len(files_objects[f]) == objects_count[f])
        i += 1
    print("success")
    # Write and check
    print("TEST: xmlWrite()")
    writeXml(files_objects, output)
    written_objects = readXml(output)
    for f in files_objects.keys():
        assert(f in written_objects.keys())
        assert(files_objects[f] == written_objects[f])
    print("success")
    print("ALL TESTS SUCCESS")
