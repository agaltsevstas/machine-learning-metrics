#!/usr/bin/env python3

import sys
import os
import shutil
import argparse
import xml.etree.ElementTree as ET
from python.shoko.basic_utils import get_classes_xml, get_fnames_xml

def main(args):

    # Check parameters   
    assert(os.path.exists(args.xmlfile))
    assert(os.path.exists(args.src_path))

    if not os.path.exists(args.dest_path):
        os.makedirs(args.dest_path)

    tree = ET.parse(args.xmlfile)
    root = tree.getroot()
    
    l_fnames = get_fnames_xml(root, True, False)
    print("Number of labeled files: {}".format(len(l_fnames)))
    
    cnt = 0
    for fname in l_fnames:
        shutil.copy2(os.path.join(args.src_path, fname), os.path.join(args.dest_path, fname))
        cnt += 1
    print("Copied {} files".format(cnt))
    
if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--xmlfile", type=str, required=True)
        parser.add_argument("--src_path", type=str, required=True)
        parser.add_argument("--dest_path", type=str, required=True)
    except Exception as ex:
        print("ERRROR: {}".format(ex))

    main(parser.parse_args(sys.argv[1:]))
