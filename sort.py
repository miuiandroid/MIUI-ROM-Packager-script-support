#!/usr/bin/env python
import os, sys, os.path

try:
    from xml.etree import ElementTree as ET
except ImportError:
    try:
        from elementtree import ElementTree as ET
    except ImportError:
        try:
            from lxml import etree as ET
        except ImportError:
            print "No usable element tree api found, install lxml or elementtree plz"
            sys.exit(1)

def indent(elem, level=0):
    """Insert whitespaces so elements are pretty printed"""
    
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

def sort_strings_file(xmlfile):
    """sort all strings within given strings.xml file"""
    
    all_strings = {}

    # read original file
    tree = ET.ElementTree()
    tree.parse(xmlfile)

    # iter over all strings, stick them into dictionary
    for element in list(tree.getroot()):
        all_strings[element.attrib['name']] = element.text

    # create new root element and add all strings sorted below
    newroot = ET.Element("resources")
    for key in sorted(all_strings.keys()):
        newstring = ET.SubElement(newroot, "string")
        newstring.attrib['name'] = key
        newstring.text = all_strings[key]

    # Re-indent new root element, aka pretty-format it
    indent(newroot)

    # write new root element back to xml file
    newtree = ET.ElementTree(newroot)
    newtree.write(xmlfile, encoding="UTF-8")
    
if __name__ == '__main__':
    for root, dirs, files in os.walk("/home/miuiandroid/public_html/rom-dev/output/build/xml_sources"):
        for filename in files:
            if filename == "strings.xml":
                realfile = os.path.join(root, filename)
                print "Sorting strings in %s" % realfile
                sort_strings_file(realfile)
