from xml.etree import ElementTree as ET
import unittest

import pytest
from unittest import mock

from distxml.distxml.base_xml_converter import BaseXMLConverter
from .utils import base_xml_tree, DATA_CONTENT

def test_init(base_xml_tree):
    assert base_xml_tree.data == [{}]
    assert base_xml_tree.sub_elements == []
    assert base_xml_tree.tree is not None
    assert base_xml_tree.root_element is not None

    assert base_xml_tree.root_element.tag == "Outer Tag"

def test_initialize_element_tree(base_xml_tree):
    new_tree, new_root = base_xml_tree._initialize_element_tree("new")
    assert type(new_tree) == ET.ElementTree
    assert type(new_root) == ET.Element
    assert new_root.tag == "new"

def test_queue(base_xml_tree):
    assert base_xml_tree.data == [{}]

    base_xml_tree.queue(DATA_CONTENT)
    assert base_xml_tree.data is not None
    assert base_xml_tree.data == DATA_CONTENT

@mock.patch("xml.etree.ElementTree.ElementTree.write")
def test_write_to_file(writer, base_xml_tree):
    base_xml_tree.write_to_file("hi")
    assert writer.call_count == 1
