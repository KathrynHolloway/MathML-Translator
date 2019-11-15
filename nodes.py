from abc import ABC, abstractmethod #note that the later is a decorator
from lxml import etree

class Node(ABC):
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes

    @abstractmethod
    def get_name(self):
        return self.name

    # @abstractmethod
    # def get_child(self):
    #     pass
    #     return self.child
    #
    # @abstractmethod
    # def get_sibling(self):
    #     pass
    #     return self.sibling
    '''add get attributes?'''

    @abstractmethod
    def outputpresxml(self):
        pass

class Value(Node):
    #values are numbers and leaves so by definition, no children
    def __init__(self, name, sibling, attributes):
        super().__init__(name, attributes)
        self.sibling = sibling

    def get_name(self):
        return self.name

    # def get_child(self):
    #     return self.child

    def get_nextchild(self):
        return self.sibling

    def outputpresxml(self, parent):
        # output the xml for this element
        mn = etree.SubElement(parent, "mn")
        mn.text = self.get_name()

class Operator(Node):
    def __init__(self, name, child0, child1, attributes):
        super().__init__(name, attributes)
        self.child0 = child0
        self.child1 = child1

    def get_name(self):
        return self.name

    def get_child(self):
        return self.child0

    def get_nextchild(self):
        return self.child1
    # operators can have siblings

    def outputpresxml(self, parent):
        if self.get_name() in ["frac", "power"]:
            #output the xml for the operator
            if self.get_name() == "power":
                mo = etree.SubElement(parent, "msup")
            else:
                mo = etree.SubElement(parent, "m" + self.get_name())

            #output the xml for the first child
            #should make sure no unecessary mrow are made but doesn't work? does now
            if type(self.get_child()) is Operator:
                print("here")
                mrow1 = etree.SubElement(mo, "mrow")
                self.get_child().outputpresxml(mrow1)
            else:
                self.get_child().outputpresxml(mo)
            # mrow1 = etree.SubElement(mo, "mrow")
            # self.get_child().outputpresxml(mrow1)

            # output the xml for the second child
            if type(self.get_nextchild()) is Operator:
                mrow2 = etree.SubElement(mo, "mrow")
                self.get_nextchild().outputpresxml(mrow2)
            else:
                self.get_nextchild().outputpresxml(mo)
            # mrow2 = etree.SubElement(mo, "mrow")
            # self.get_nextchild().outputpresxml(mrow2)


        elif self.get_nextchild() == None : # eg sqrt, -b where op needs to be made first
            # output the xml for the operator

            if self.get_name() in ["sqrt"]:
                mo = etree.SubElement(parent, "msqrt")
                mrow = etree.SubElement(mo, "mrow")
                # first output the xml for only child
                self.get_child().outputpresxml(mrow)
            else:
                mrow = etree.SubElement(parent, "mrow")
                mo = etree.SubElement(mrow, "mo")
                mo.text = self.get_name()
                #output the xml for only child
                self.get_child().outputpresxml(mrow)

        else:
            # first output the xml for child0
            self.get_child().outputpresxml(parent)

            #second output the xml for the operator
            mo = etree.SubElement(parent,"mo")
            mo.text = self.get_name()
            ''' TO DO
            Add logic for tags such as mfrac or msqrt'''

            #third output the xml for child1
            self.get_nextchild().outputpresxml(parent)


class Identifier(Node):
    def __init__(self, name, sibling, attributes):
        super().__init__(name, attributes)
        self.sibling = sibling

    def get_name(self):
        return self.name
    
    # def get_child(self):
    #     return self.child
    #is a leaf so by definition cannot have a child

    def get_nextchild(self):
        return self.sibling

    def outputpresxml(self, parent):
        # output the xml for this element
        mi = etree.SubElement(parent, "mi")
        mi.text = self.get_name()
