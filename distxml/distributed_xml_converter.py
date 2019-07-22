from xml.etree import ElementTree as ET
import ray
from distxml.distxml.base_xml_converter import BaseXMLConverter





class DistributedXMLConverter(BaseXMLConverter):
    """
    Class for converting data into xml, without distributing the workload.

    Attributes:
        - tree {xml.etree.ElementTree.ElementTree}: The xml tree object
        - root_element {xml.etree.ElementTree.Element}: The root element of
            the xml tree
        - sub_elements {list(xml.etree.ElementTree.Element)}: List of
            sub-element xml objects, that the root element can extend
            within (initially an empty list, until_create_sub_element_list
            has been run)
        - data {list(dict)}: data currently queue to become sub-elements of
            the root element

    Extends:
        BaseXMLConverter
    """

    def __init__(self, outer_tag):
        BaseXMLConverter.__init__(self, outer_tag)


    def _create_sub_element_list(self, sub_element_tag):
        sub_elements = []

        for element_content in self.data:
            cur_tag = sub_element_tag
            cur_content = element_content
            sub_element = _create_sub_element.remote(cur_tag, cur_content)
            sub_elements.append(sub_element)

        self.sub_elements = ray.get(sub_elements)

@ray.remote
def _create_innermost_element(tag, text=None):
    """ Creates a simple element

    Builds a simple xml element of only a tag and inner text

    Arguments:
        tag {str} -- The xml element's tag

    Keyword Arguments:
        text {str} -- The text within the xml element (default: {None})

    Returns:
        xml.etree.ElementTree.Element -- The xml element
    """
    element = ET.Element(tag)
    if text:
        element.text=text

    return element

@ray.remote
def _create_sub_element(sub_element_tag, element_content):
    """ Creates a subelement

    Given a tag and content, creates an element with that tag and with
    inner tags as described in element content.

    Arguments:
        element_tag {str} -- The tag of the subelement
            element_content {dict} -- A dictionary of the elements contained in the sub-element. The keys are the tags of those
            inner elements, and the values are the text within them.
    """

    inner_elements = []
    outer_element = ET.Element(sub_element_tag)

    for inner_element_tag in element_content.keys():
        current_content = element_content[inner_element_tag]
        sub_element = _create_innermost_element.remote(inner_element_tag, current_content)
        inner_elements.append(sub_element)

    inner_elements = ray.get(inner_elements)
    outer_element.extend(inner_elements)

    return outer_element




