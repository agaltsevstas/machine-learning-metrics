#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cv2
import sys
import os
import numpy as np
import pm_utils as pm

# Expected arguments
expected = ["images path", "ratio"] # ratio = width / height
values = np.array(["", ""])
description = "Remove broken images and images with ratio less then specified"
values = pm.parseArguments(sys.argv, expected, values, __file__, description)

images_path = values[0]
ratio_expected = float(values[1])

l_fnames = os.listdir(images_path)
num_files_all = len(l_fnames)
print("Number of files: {}".format(num_files_all))

# remove broken files
cnt_broken = 0
cnt_ratio_bad = 0
for fname in l_fnames:
    img = cv2.imread(os.path.join(images_path, fname))
    if img is None:
        cnt_broken += 1
        os.remove(os.path.join(images_path, fname))
        continue
    ratio_cur = img.shape[1] / img.shape[0]
    if ratio_cur < ratio_expected:
        cnt_ratio_bad += 1
        os.remove(os.path.join(images_path, fname))

print("Number of broken files: {}".format(cnt_broken))
print("Number of bad ratio files: {}".format(cnt_ratio_bad))

