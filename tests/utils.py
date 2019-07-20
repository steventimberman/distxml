import pytest
from unittest import mock

from distxml.distxml.base_xml_converter import BaseXMLConverter
from distxml.distxml.xml_converter import XMLConverter


DATA_TAG = "hellogoodbye"
INNER_TAG_1 = "Hello"
INNER_TAG_2 = "Bye"
INNER_TEXT_1 = "Hi there"
INNER_TEXT_2 = "Bye there"

DATA_CONTENT = [{INNER_TAG_1: INNER_TEXT_1, INNER_TAG_2:INNER_TEXT_2}]
DATA_CONTENT_MULTIPLE = [
    {INNER_TAG_1: INNER_TEXT_1, INNER_TAG_2:INNER_TEXT_2},
    {INNER_TAG_2: INNER_TEXT_2, INNER_TAG_1:INNER_TEXT_1}
    ]

XML_STRING_1 = (
    "<hellogoodbye><Hello>Hi there</Hello><Bye>Bye there</Bye></hellogoodbye>"
)

XML_STRING_2 = (
    "<hellogoodbye><Bye>Bye there</Bye><Hello>Hi there</Hello></hellogoodbye>"
)

DATA_XML_STRING = XML_STRING_1

DATA_XML_STRING_COMPLETE = "<Outer Tag>{}{}</Outer Tag>".format(
    XML_STRING_1, XML_STRING_2
)

@pytest.fixture
def base_xml_tree():
    tree = BaseXMLConverter("Outer Tag")
    return tree

@pytest.fixture
def xml_tree():
    tree = XMLConverter("Outer Tag")
    return tree

@pytest.fixture
def distributed_xml_tree():
    mock.patch("ray.init")
    tree = DistributedXMLConverter.remote("Outer Tag")
    return tree

@pytest.fixture
def inner_element_no_text(xml_tree):
    inner_element = xml_tree._create_innermost_element("Inner")
    return inner_element

@pytest.fixture
def inner_element_with_text(xml_tree):
    inner_element = xml_tree._create_innermost_element("Inner", "Inner text")
    return inner_element

@pytest.fixture
def outer_element(xml_tree):
    outer_element = xml_tree._create_sub_element(DATA_TAG, DATA_CONTENT[0])
    return outer_element

