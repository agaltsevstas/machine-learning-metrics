import os
import xml.etree.ElementTree as ET

# Парсинг xml файла
def read_xml(xmlpath, naming="basename"):
    result = dict()
    tree = ET.parse(xmlpath)
    root = tree.getroot()
    assert(root.tag == "list")
    for file_node in root:
        if file_node.tag != "file":
            continue
        # Получение элементов
        objects = []
        for object_node in file_node:   
            if object_node.tag != "object":
                continue
            classname = object_node.attrib["className"]
            x = int(object_node.attrib["x"])
            y = int(object_node.attrib["y"])
            width = int(object_node.attrib["width"])
            height = int(object_node.attrib["height"])
            cls = classname
            objects.append([x, y, width, height, cls])
        # Найти изображение и создать текстовый файл рядом с ним
        #relpath = os.path.relpath(file_node.attrib["path"].replace('\\', '/'), os.path.dirname(xmlpath))
        #relpath = file_node.attrib["path"].replace('\\', '/')
        path = file_node.attrib["path"].replace('\\', '/')
        if naming == "basename":
            path = os.path.basename(file_node.attrib["path"])
        elif naming == "absolute":
            path = os.path.abspath(os.path.join(os.path.dirname(xmlpath), path))
        elif "/" in path:
            path = os.path.relpath(file_node.attrib["path"].replace('\\', '/'), os.path.dirname(xmlpath))
        result[path] = objects
    return result

# Xml файл с новыми строками
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
    for filename in objects.keys():
        file_tag = ET.SubElement(root, "file")
        file_tag.set("path", filename)
        if list_viewed is not None and filename in list_viewed:
            file_tag.set("viewed", "1")
        for obj in objects[filename]:
            object_tag = ET.SubElement(file_tag, "object")            
            object_tag.set('className', obj[4])
            object_tag.set('x', str(obj[0]))
            object_tag.set('y', str(obj[1]))
            object_tag.set('width', str(obj[2]))
            object_tag.set('height', str(obj[3]))
    tree = ET.ElementTree(root)
    root = indent(root)    
    tree.write(filepath)