import os
import xml.etree.ElementTree as ET

# Чтение xml файла
def read_xml(xmlpath, naming="basename"):
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
        for object_node in filenode:   
            if object_node.tag != "object":
                continue
            classname = object_node.attrib["className"]
            x = int(object_node.attrib["x"])
            y = int(object_node.attrib["y"])
            width = int(object_node.attrib["width"])
            height = int(object_node.attrib["height"])
            cls = classname
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

# xml файл с новыми строками
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

# Запись в xml файл
def write_xml(objects, filepath, list_viewed=None):
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