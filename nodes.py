from abc import ABC, abstractmethod #note that the later is a decorator
from lxml import etree
from xmlout import translatecname, translatepname
import html

class Node(ABC):
    def __init__(self, attributes):
        self.attributes = attributes

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
    def get_attributes(self):
        return  self.attributes

    @abstractmethod
    def outputpresxml(self):
        pass

class Value(Node):
    #values are numbers and leaves so by definition, no children
    def __init__(self, name, sibling, attributes):
        super().__init__(attributes)
        self.name = name
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
        mn.text = html.unescape(self.get_name())

    def outputcontxml(self,parent):
        # output the xml for this element
        cn = etree.SubElement(parent, "cn")
        cn.text = self.get_name()

class Operator(Node):
    def __init__(self, name, child0, child1, attributes):
        super().__init__(attributes)
        self.name = name
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
        #make the op first, has 2 children?
        if self.get_name().strip() in ["/", "power"]:
            #output the xml for the operator
            mo = etree.SubElement(parent, translatepname(self.get_name().strip()))



            #output the xml for the first child
            #should make sure no unecessary mrow are made but doesn't work? does now
            if type(self.get_child()) is Operator:
                mrow1 = etree.SubElement(mo, "mrow")
                self.get_child().outputpresxml(mrow1)
            else:
                self.get_child().outputpresxml(mo)

            # output the xml for the second child
            if type(self.get_nextchild()) is Operator:
                mrow2 = etree.SubElement(mo, "mrow")
                self.get_nextchild().outputpresxml(mrow2)
            else:
                self.get_nextchild().outputpresxml(mo)
        elif self.get_name().strip() in ["sin", "cos", "tan"]:
            #these have been represented using operators but are actually identifiers in pres ML
            # output the xml for this element
            mi = etree.SubElement(parent, "mi")
            mi.text = self.get_name()

            mo = etree.SubElement(parent, "mo")
            mo.text = html.unescape("&#8289;") #function application

            #output the child
            self.get_child().outputpresxml(parent)


        elif self.get_nextchild() == None : # eg sqrt, -b and other unary operators
            #output xml for it's first and only child then the operator
            if self.get_name().strip() in ["!"]:
                mrow = etree.SubElement(parent, "mrow")
                self.get_child().outputpresxml(mrow)
                mo = etree.SubElement(mrow, "mo")
                mo.text = translatepname(self.get_name().strip())
            #special operator first eg sqrt, then its first and only child
            if self.get_name().strip() in ["sqrt"]:
                mrow = etree.SubElement(parent, "mrow")
                mo = etree.SubElement(mrow, translatepname(self.get_name().strip()))
                # output the xml for only child
                self.get_child().outputpresxml(mo)
            #operator first, then its first and only child
            else:
                mrow = etree.SubElement(parent, "mrow")
                mo = etree.SubElement(mrow, "mo")
                mo.text = html.unescape(translatepname(self.get_name().strip()))
                #output the xml for only child
                self.get_child().outputpresxml(mrow)

        else:
            # first output the xml for child0
            self.get_child().outputpresxml(parent)

            #second output the xml for the operator
            mo = etree.SubElement(parent,"mo")
            mo.text = html.unescape(translatepname(self.get_name().strip()))

            #third output the xml for child1
            self.get_nextchild().outputpresxml(parent)

    def outputcontxml(self,parent):
        apply = etree.SubElement(parent, "apply")
        op = etree.SubElement(apply, translatecname(self.get_name().strip()))
        self.get_child().outputcontxml(apply)

        try:
            if self.get_nextchild().get_name().strip() == self.get_name().strip():
                self.get_nextchild().outputnextcontxml(apply, self.get_name().strip())
            else:
                self.get_nextchild().outputcontxml(apply)
        except AttributeError:
            pass


    def outputnextcontxml(self, parent, prevop):
        #mamke the lhs child
        self.get_child().outputcontxml(parent)
        #check the rhs child
        if self.get_nextchild().get_name().strip() == prevop :
            self.get_nextchild().outputnextcontxml(parent, prevop)

        else:
            # make last rhs child
            self.get_nextchild().outputcontxml(parent)

class Brackets(Node):
    def __init__(self, openbracket , closebracket, child0, attributes):
        super().__init__(attributes)
        self.openbracket = openbracket
        self.closebracket = closebracket
        self.child0 = child0

    def get_openbrac(self):
        return self.openbracket

    def get_closebrac(self):
        return self.closebracket

    def get_child(self):
        return self.child0

    def outputpresxml(self, parent):
        mrow = etree.SubElement(parent, "mrow")
        moopen = etree.SubElement(mrow, "mo")
        moopen.text = html.unescape(self.get_openbrac())
        # output the xml for only child
        self.get_child().outputpresxml(mrow)
        moclose = etree.SubElement( mrow, "mo")
        moclose.text = html.unescape(self.get_closebrac())

    def outputcontxml(self,parent):
        print("implement")

class Interval(Node):
    def __init__(self, openbracket, closebracket , child, attributes):
        super().__init__(attributes)
        self.openbracket = openbracket
        self.closebracket = closebracket
        self.child= child

    def get_openbrac(self):
        return self.openbracket
    def get_closebrac(self):
        return self.closebracket
    def get_child(self):
        return self.child

    def outputpresxml(self,parent):
        mrow = etree.SubElement(parent, "mrow")
        moopen = etree.SubElement(mrow, "mo")
        moopen.text = html.unescape(self.get_openbrac())
        # output the xml for only child
        self.get_child().outputpresxml(mrow)
        moclose = etree.SubElement(mrow, "mo")
        moclose.text = html.unescape(self.get_closebrac())

    def outputcontxml(self,parent):
        apply = etree.SubElement(parent, "apply")
        # try:
        #     closuretype = self.get_attributes().get("closure")
        # except TypeError:
        #     closuretype = "closed"
        # interval = etree.SubElement(apply, "interval", closure = closuretype)
        try:
            interval = etree.SubElement(apply, "interval", closure=self.get_attributes().get("closure"))
        except TypeError:
            interval = etree.SubElement(apply, "interval", closure="closed")
        self.get_child().get_child().outputcontxml(apply)
        self.get_child().get_nextchild().outputcontxml(apply)




class Identifier(Node):
    def __init__(self, name, sibling, attributes):
        super().__init__(attributes)
        self.name = name
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
        mi.text = html.unescape(self.get_name())

    def outputcontxml(self,parent):
        # output the xml for this element
        ci = etree.SubElement(parent, "ci")
        ci.text = self.get_name()