#!/usr/bin/env python

from shutil import copyfile
import os

comment_parser = None # use default parser
try:
    from lxml import etree as ET
except ImportError:
    import xml.etree.ElementTree as ET
    # keeps comments when parsing with xml
    # (lxml automatically preserves comments & is recommended)
    # MAY NOT WORK FOR Python 3! Sorry!
    # credit: https://stackoverflow.com/a/34324359
    class CommentedTreeBuilder(ET.TreeBuilder):
        def __init__(self, *args, **kwargs):
            super(CommentedTreeBuilder, self).__init__(*args, **kwargs)
        def comment(self, data):
            self.start(ET.Comment, {})
            self.data(data)
            self.end(ET.Comment)
    comment_parser = ET.XMLParser(target=CommentedTreeBuilder())

CONFIG_FILE = '/usr/share/tomcat8/conf/server.xml'

CHANGES = [
    {
        'path': './/Connector',
        'target_attrs': {
            'port': '8009'
        },
        'updated_attrs': {
            'enableLookups': 'false',
            'tomcatAuthentication': 'false',
            'address': '127.0.0.1'
        }
    }
]

def matches_attrs(el, target_attrs):
    return all(el.attrib.get(k) == v for k, v in target_attrs.items())

def remove_element(root, el):
    # create a lookup for subelement -> element
    # credit https://stackoverflow.com/a/20132342
    parent_map = {c:p for p in root.iter() for c in p}
    parent_map[el].remove(el)

def change_xml_attrs(filename, changes, backup=True, parser=None):
    try:
        data = ET.parse(filename, parser=parser)
    except ET.ParseError:
        if not parser:
            raise
        # try using default parser
        data = ET.parse(filename)

    if backup:
        copyfile(filename, '{}.orig'.format(filename))

    root = data.getroot()

    for change in changes:
        print("Doing change", change)
        for el in root.iterfind(change['path']):
            target_attrs = change.get('target_attrs')
            if not target_attrs or matches_attrs(el, target_attrs):
                print(el, "is a match!")
                if change.get('updated_attrs'):
                    print("I will update the attributes")
                    el.attrib.update(change['updated_attrs'])
                elif change.get('action') == 'DELETE':
                    print("I will delete the element")
                    remove_element(root, el)
    try:
        data.write(filename)
    except:
        # if an error occurs while writing the new file, restore the old one
        copyfile('{}.orig'.format(filename), filename)

change_xml_attrs(CONFIG_FILE, CHANGES, parser=comment_parser)
