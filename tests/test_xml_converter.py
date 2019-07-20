from xml.etree import ElementTree as ET
import unittest

import pytest
from unittest import mock

from distxml.distxml.base_xml_converter import BaseXMLConverter
from distxml.distxml.xml_converter import XMLConverter

from .utils import (
    base_xml_tree, xml_tree,
    inner_element_with_text, inner_element_no_text, outer_element,
    DATA_TAG, DATA_CONTENT, DATA_CONTENT_MULTIPLE,
    DATA_XML_STRING, DATA_XML_STRING_COMPLETE,
    INNER_TAG_1, INNER_TEXT_1, INNER_TAG_2, INNER_TEXT_2
)


def test_init(xml_tree):
    assert xml_tree.data == [{}]
    assert xml_tree.sub_elements == []
    assert xml_tree.tree is not None
    assert xml_tree.root_element is not None

    assert xml_tree.root_element.tag == "Outer Tag"



def test_initialize_element_tree(xml_tree):
    new_tree, new_root = xml_tree._initialize_element_tree("new")
    assert type(new_tree) == ET.ElementTree
    assert type(new_root) == ET.Element
    assert new_root.tag == "new"

def test_queue(xml_tree):
    assert xml_tree.data == [{}]

    xml_tree.queue(DATA_CONTENT)
    assert xml_tree.data is not None
    assert xml_tree.data == DATA_CONTENT


@mock.patch("xml.etree.ElementTree.ElementTree.write")
def test_write_to_file(writer, xml_tree):
    xml_tree.write_to_file("hi")
    assert writer.call_count == 1


def test_create_innermost_element(xml_tree, inner_element_no_text):
    assert type(inner_element_no_text) == ET.Element
    assert inner_element_no_text.tag == "Inner"
    assert inner_element_no_text.text == None


def test_create_innermost_element_with_text(inner_element_with_text):
    assert type(inner_element_with_text) == ET.Element
    assert inner_element_with_text.tag == "Inner"
    assert inner_element_with_text.text == "Inner text"

def test_create_sub_element(outer_element):
    self_and_children = [i for i in outer_element.iter()]
    assert outer_element.tag == DATA_TAG
    assert len(self_and_children) == 3
    assert self_and_children[0] == outer_element
    assert self_and_children[1].tag == INNER_TAG_1
    assert self_and_children[1].text == INNER_TEXT_1
    assert self_and_children[2].tag == INNER_TAG_2
    assert self_and_children[2].text == INNER_TEXT_2

def test__str__and__repr__(xml_tree, outer_element):

    xml_tree.tree = ET.ElementTree(element=outer_element)
    xml_tree.root_element = outer_element

    string_rep = DATA_XML_STRING

    assert xml_tree.__str__() == string_rep
    assert xml_tree.__repr__() == string_rep

def test_create_sub_element_list(xml_tree, outer_element):
    xml_tree.data = DATA_CONTENT_MULTIPLE
    xml_tree._create_sub_element_list("hellogoodbye")
    assert len(xml_tree.sub_elements) == 2

    sub_element_1_children = [i for i in xml_tree.sub_elements[0].iter()][1:]
    sub_element_2_children = [i for i in xml_tree.sub_elements[1].iter()][1:]


    assert sub_element_1_children[0].tag == INNER_TAG_1
    assert sub_element_1_children[0].text == INNER_TEXT_1
    assert sub_element_1_children[1].tag == INNER_TAG_2
    assert sub_element_1_children[1].text == INNER_TEXT_2

    assert sub_element_2_children[0].tag == INNER_TAG_2
    assert sub_element_2_children[0].text == INNER_TEXT_2
    assert sub_element_2_children[1].tag == INNER_TAG_1
    assert sub_element_2_children[1].text == INNER_TEXT_1



def test_compile_and_string(xml_tree):
    xml_tree.data = DATA_CONTENT_MULTIPLE
    xml_tree._create_sub_element_list("hellogoodbye")

    assert len(xml_tree.sub_elements) == 2

    xml_tree.compile()

    assert len(xml_tree.sub_elements) == 0
    assert xml_tree.data == [{}]

    assert xml_tree.__str__() == DATA_XML_STRING_COMPLETE
