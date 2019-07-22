from xml.etree import ElementTree as ET
import unittest

import pytest
import ray
from unittest import mock

from distxml.distxml.base_xml_converter import BaseXMLConverter
from distxml.distxml.distributed_xml_converter import (
    DistributedXMLConverter,
    _create_innermost_element,
    _create_sub_element
)

from .utils import (
    base_xml_tree,
    # distributed_xml_tree,
    # dist_inner_element_with_text, dist_inner_element_no_text, dist_outer_element,
    DATA_TAG, DATA_CONTENT, DATA_CONTENT_MULTIPLE,
    DATA_XML_STRING, DATA_XML_STRING_COMPLETE,
    INNER_TAG_1, INNER_TEXT_1, INNER_TAG_2, INNER_TEXT_2
)

def make_dist_xml_converter():
    tree = DistributedXMLConverter("Outer Tag")
    return tree

def test_init():
    ray.init()
    distributed_xml_tree = make_dist_xml_converter()
    assert distributed_xml_tree.data == [{}]
    assert distributed_xml_tree.sub_elements == []
    assert distributed_xml_tree.tree is not None
    assert distributed_xml_tree.root_element is not None
    assert ray.is_initialized()

    assert distributed_xml_tree.root_element.tag == "Outer Tag"

    ray.shutdown()
    assert not ray.is_initialized()

def test_initialize_element_tree():
    ray.init()
    distributed_xml_tree = make_dist_xml_converter()
    new_tree, new_root = distributed_xml_tree._initialize_element_tree("new")
    assert type(new_tree) == ET.ElementTree
    assert type(new_root) == ET.Element
    assert new_root.tag == "new"
    ray.shutdown()

    assert not ray.is_initialized()

def test_queue():
    ray.init()
    distributed_xml_tree = make_dist_xml_converter()

    assert distributed_xml_tree.data == [{}]
    distributed_xml_tree.queue(DATA_CONTENT)
    assert distributed_xml_tree.data is not None
    assert distributed_xml_tree.data == DATA_CONTENT
    ray.shutdown()
    assert not ray.is_initialized()

@mock.patch("xml.etree.ElementTree.ElementTree.write")
def test_write_to_file(writer):
    ray.init()
    distributed_xml_tree = make_dist_xml_converter()

    distributed_xml_tree.write_to_file("hi")
    assert writer.call_count == 1
    ray.shutdown()
    assert not ray.is_initialized()

def test_create_innermost_element():

    ray.init()
    distributed_xml_tree = make_dist_xml_converter()

    try:
        inner_elements = _create_innermost_element.remote("Inner", None)

        inner_element_returned = ray.get(inner_elements)

        assert type(inner_element_returned) == ET.Element
        assert inner_element_returned.tag == "Inner"
        assert inner_element_returned.text == None

    except:
        ray.shutdown()
        assert False

    else:
        ray.shutdown()
        assert not ray.is_initialized()



def test_create_sub_element():
    ray.init()
    distributed_xml_tree = make_dist_xml_converter()

    try:

        outer_element = _create_sub_element.remote(DATA_TAG, DATA_CONTENT[0])
        outer_element = ray.get(outer_element)

        self_and_children = [i for i in outer_element.iter()]

        assert outer_element.tag == DATA_TAG
        assert len(self_and_children) == 3
        assert self_and_children[0] == outer_element
        assert self_and_children[1].tag == INNER_TAG_1
        assert self_and_children[1].text == INNER_TEXT_1
        assert self_and_children[2].tag == INNER_TAG_2
        assert self_and_children[2].text == INNER_TEXT_2

    except:
        ray.shutdown()
        assert not ray.is_initialized()
        assert False

    else:

        ray.shutdown()
        assert not ray.is_initialized()

def test_create_sub_element_list():
    ray.init()
    distributed_xml_tree = make_dist_xml_converter()

    try:
        outer_element = _create_sub_element.remote(DATA_TAG, DATA_CONTENT[0])
        outer_element = ray.get(outer_element)

        distributed_xml_tree.data = DATA_CONTENT_MULTIPLE
        distributed_xml_tree._create_sub_element_list("hellogoodbye")
        assert len(distributed_xml_tree.sub_elements) == 2

        sub_element_1_children = [i for i in distributed_xml_tree.sub_elements[0].iter()][1:]
        sub_element_2_children = [i for i in distributed_xml_tree.sub_elements[1].iter()][1:]


        assert sub_element_1_children[0].tag == INNER_TAG_1
        assert sub_element_1_children[0].text == INNER_TEXT_1
        assert sub_element_1_children[1].tag == INNER_TAG_2
        assert sub_element_1_children[1].text == INNER_TEXT_2

        assert sub_element_2_children[0].tag == INNER_TAG_2
        assert sub_element_2_children[0].text == INNER_TEXT_2
        assert sub_element_2_children[1].tag == INNER_TAG_1
        assert sub_element_2_children[1].text == INNER_TEXT_1

    except:
        ray.shutdown()
        assert not ray.is_initialized()
        assert False

    else:
        ray.shutdown()
        assert not ray.is_initialized()

def test_compile_and_string():
    ray.init()
    distributed_xml_tree = make_dist_xml_converter()

    try:
        distributed_xml_tree.data = DATA_CONTENT_MULTIPLE

        assert len(distributed_xml_tree.data) == 2

        distributed_xml_tree.compile("hellogoodbye")

        assert len(distributed_xml_tree.sub_elements) == 0
        assert distributed_xml_tree.data == [{}]

        assert distributed_xml_tree.__str__() == DATA_XML_STRING_COMPLETE

    except:
        ray.shutdown()
        assert not ray.is_initialized()
        assert False

    else:
        ray.shutdown()
        assert not ray.is_initialized()

def test__str__and__repr__():
    ray.init()
    distributed_xml_tree = make_dist_xml_converter()

    try:
        outer_element = _create_sub_element.remote(DATA_TAG, DATA_CONTENT[0])
        outer_element = ray.get(outer_element)

        distributed_xml_tree.tree = ET.ElementTree(element=outer_element)
        distributed_xml_tree.root_element = outer_element

        string_rep = DATA_XML_STRING

        assert distributed_xml_tree.__str__() == string_rep
        assert distributed_xml_tree.__repr__() == string_rep

    except:
        ray.shutdown()
        assert not ray.is_initialized()
        assert False

    else:
        ray.shutdown()
        assert not ray.is_initialized()


