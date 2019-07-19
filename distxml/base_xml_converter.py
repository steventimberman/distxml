from xml.etree import ElementTree as ET

class BaseXMLConverter:
    """ Base XMLConverter class, for others to inherit from.

        Arguement:
            data (list(dict)): a list of objects, represented as a dictionary.
                These represent the xml elements that will be created
            outer_tag (str): A string that will be used as the tag of the
                outermost xml element.
    """
    def __init__(self, data=[{}], outer_tag):
        self.tree, self.root_element = self._initialize_element_tree(outer_tag)
        self.data = data


    def _initialize_element_tree(self, outer_tag):
        root_element = ET.Element(outer_tag)
        element_tree = ET.ElementTree(element=root_element)
        return element_tree, root_element

