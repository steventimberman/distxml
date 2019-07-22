from xml.etree import ElementTree as ET

class BaseXMLConverter:
    """ Base XMLConverter class, for others to inherit from.

        Arguement:
            data (list(dict)): a list of objects, represented as a dictionary.
                These represent the xml elements that will be created
            outer_tag (str): A string that will be used as the tag of the
                outermost xml element.
    """
    def __init__(self, outer_tag):
        self.data = [{}]
        self.tree, self.root_element = self._initialize_element_tree(outer_tag)
        self.sub_elements = []


    def _initialize_element_tree(self, outer_tag):
        root_element = ET.Element(outer_tag)
        element_tree = ET.ElementTree(element=root_element)
        return element_tree, root_element

    def queue(self, data):
        err_message = (
            "Input data must be a python list of at least 1 dictionary objects"
        )
        if type(data) != list:
            raise Exception(err_message)
        elif len(data) < 1:
            raise Exception(err_message)
        elif type(data[0]) != dict:
            raise Exception(err_message)

        self.data = data
        print("--------- Queueing ---------------------------")
        print("Data Queued!")
        print("{} sub-elements ready to be compiled!".format(len(data)))
        print("------------------------------------------------")


    def compile(self, sub_element_tag):
        print("--------- Compiling ----------------------------")
        print("Converting queue to sub-elements")
        print("...")
        self._create_sub_element_list(sub_element_tag)
        count = len(self.sub_elements)
        print("Extending root element with sub-elements!")
        print("...")
        self.root_element.extend(self.sub_elements)
        self.sub_elements = []
        self.data = [{}]
        print("{} sub-elements added! No sub-elements queued.".format(count))
        print("------------------------------------------------")

    def write_to_file(self, file_name):
        """ Writes Element Tree to file

        Takes in entire filename (including extention), and writes Element Tree
        to that file.

        Arguments:
            filename {[type]} -- [description]
        """
        self.tree.write(file_name)

    def __str__(self):
        # return ("hi")
        return ET.tostring(self.tree.getroot(), 'utf-8', method="xml").decode("utf-8", "replace")


    def __repr__(self):
        return ET.tostring(self.tree.getroot(), 'utf-8', method="xml").decode("utf-8", "replace")

