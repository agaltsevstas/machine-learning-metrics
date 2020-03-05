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
expected = ["source xml path", "processed xml path"]
values = np.array(["", ""])
description = "Compares two lists to measure quality"
values = pm.parseArguments(sys.argv, expected, values, __file__, description)

# Validation
xmlfiles = [values[0], values[1]]
assert(os.path.exists(xmlfiles[0]))
assert(os.path.exists(xmlfiles[1]))

# Function
files_objects = [pm.readXml(fpath, "basename") for fpath in xmlfiles]

class Metrics:
    def __init__(self):
        self.tp = 0
        self.fp = 0
        self.tn = 0
        self.fn = 0
    def number(self):
        return self.tp + self.fn
    def accuracy(self):
        sum = self.tp + self.fp + self.tn + self.fn
        if sum == 0:
            return 0
        return (self.tp + self.tn) / sum
    def prec(self):
        sum = self.tp + self.fp
        if sum == 0:
            return 0
        return self.tp / sum
    def recall(self):
        sum = self.tp + self.fn
        if sum == 0:
            return 0
        return self.tp / sum
    def __str__(self):
        num = 1
        if self.number() > 0:
            num = self.number()
        return "%0.2f\t%0.2f\t%0.2f\t%0.2f\t%0.2f"%(1.0*self.fn/num, self.fp/num, self.accuracy(), self.prec(), self.recall())
    @staticmethod
    def strHeader():
        result = "%10s\t%s\t%s\t%s\t%s\t%s"%("CLASSNAME", "fn", "fp", "acc", "prec", "recall")
        result = "----------------------------------------------------------\n" + result
        return result

qualities = {}

for src_file in files_objects[0]:
    src_objects = files_objects[0][src_file]
    proc_objects = []
    #print(src_file)
    for proc_file in files_objects[1]:
        if proc_file == src_file:
            proc_objects = files_objects[1][proc_file]
            break
    if proc_file != src_file:
        continue
    # Image not found in processed list
    if len(proc_objects) == 0:
        continue
    #print(src_file)
    #print(src_objects, proc_objects)
    # Objects loops
    src_pairs = np.zeros(len(src_objects), np.int32)
    proc_pairs = np.zeros(len(proc_objects), np.int32)
    for i in range(len(src_objects)):
        src_class = src_objects[i][4]
        if not src_class in qualities:
            qualities[src_class] = Metrics()
        for j in range(len(proc_objects)):
            proc_class = proc_objects[j][4]
            # True positive
            if src_class == proc_class and pm.same(src_objects[i], proc_objects[j], 0.3):
                src_pairs[i] = 1
                proc_pairs[j] = 1
                qualities[src_class].tp += 1
    # False positive
    for j in range(len(proc_objects)):
        if proc_pairs[j] == 0:
            proc_class = proc_objects[j][4]
            if not proc_class in qualities:
                qualities[proc_class] = Metrics()
            qualities[proc_class].fp += 1
    # False negative
    for j in range(len(src_objects)):
        if src_pairs[j] == 0:
            src_class = src_objects[j][4]
            qualities[src_class].fn += 1
        #print(src_pairs, proc_pairs)
    #break


print(Metrics.strHeader())
for classname in qualities:
    print( "%10s\t%s"%(classname, str(qualities[classname])) )



