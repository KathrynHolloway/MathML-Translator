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

    def set_name(self, newname):
        self.name = newname

    def get_child(self):
        return self.child0

    def get_nextchild(self):
        return self.child1
    # operators can have siblings

    def outputpresxml(self, parent):
        #make the op first, has 2 children
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
        #functions that have one child
        elif self.get_name().strip() in ["sin", "cos", "tan","ln"]:
            #these have been represented using operators but are actually identifiers in pres ML
            # output the xml for this element
            mi = etree.SubElement(parent, "mi")
            mi.text = self.get_name()

            mo = etree.SubElement(parent, "mo")
            mo.text = html.unescape("&#8289;") #function application

            #output the child
            self.get_child().outputpresxml(parent)

        # for those that from content, become mfenced elements and require a prefix
        elif self.get_name().strip() in ["gcd", "lcm", "arg"]:
            info = translatepname(self.get_name())

            # add the prefix
            mrow = etree.SubElement(parent, "mrow")
            mi = etree.SubElement(mrow, "mi")
            mi.text = info[0]

            # add the operator, function application
            functionapplication = etree.SubElement(parent, "mo")
            functionapplication.text = html.unescape("&#x2061;")

            # add the list using mfenced
            mrow1 = etree.SubElement(parent, "mrow")
            mo = etree.SubElement(mrow1, "mfenced", open=info[1], close=info[2], separators=info[3])

            # output list elements
            self.get_child().outputpresxml(mo)
            try:
                if self.get_nextchild().get_name().strip() == self.get_name().strip():
                    self.get_nextchild().outputnextpresxml(mo, self.get_name().strip())
                else:
                    self.get_nextchild().outputpresxml(mo)
            except AttributeError:
                pass
        #elements that have no second child, maybe also no first child (eg setof complexes)
        elif self.get_nextchild() == None : # eg sqrt, -b and other UNARY operators
            #output xml for it's first and only child then the operator
            if self.get_name().strip() in ["!"]:
                mrow = etree.SubElement(parent, "mrow")
                self.get_child().outputpresxml(mrow)
                mo = etree.SubElement(mrow, "mo")
                mo.text = translatepname(self.get_name())
            #special operator first eg sqrt, then its first and only child
            elif self.get_name().strip() in ["sqrt"]:
                mrow = etree.SubElement(parent, "mrow")
                mo = etree.SubElement(mrow, translatepname(self.get_name()))
                # output the xml for only child
                self.get_child().outputpresxml(mo)
            #for those that from content, become mfenced elements and require no prefix
            elif self.get_name().strip() in ["abs"]:
                mrow = etree.SubElement(parent, "mrow")
                name = translatepname(self.get_name())
                if len(name)<3:
                    seps = ""
                else:
                    seps = name[2]
                mo = etree.SubElement(mrow, "mfenced",open = name[0], close = name[1], separators = seps )
                self.get_child().outputpresxml(mo)

            elif self.get_name().strip() == "floor":
                mrow = etree.SubElement(parent, "mrow")
                openmo = etree.SubElement(mrow, "mo")
                openmo.text = html.unescape(translatepname(self.get_name())[0])

                self.get_child().outputpresxml(mrow)

                closemo = etree.SubElement(mrow, "mo")
                closemo.text = html.unescape(translatepname(self.get_name())[1])
            #no children
            elif self.get_child()==None:
                #should be some sort of constant or symbol element which has a double struck style
                constantsandsymbols = ["complexes", "integers","naturalnumbers", "primes","rationals","reals"]
                if self.get_name() in constantsandsymbols:
                    #output the element as an identifier with attribute mathvariant = "double-struck"
                    mi = etree.SubElement(parent, "mi", mathvariant = "double-struck")
                    mi.text = translatepname(self.get_name())
                else:
                    #else just use the html entity equivalent
                    mi = etree.SubElement(parent, "mi")
                    mi.text = html.unescape(translatepname(self.get_name()))

            #operator first, then its first and only child
            else:
                mrow = etree.SubElement(parent, "mrow")
                mo = etree.SubElement(mrow, "mo")
                mo.text = html.unescape(translatepname(self.get_name()))
                #output the xml for only child
                self.get_child().outputpresxml(mrow)

        else:
            # first output the xml for child0
            mrow1 = etree.SubElement(parent, "mrow")
            self.get_child().outputpresxml(mrow1)

            #second output the xml for the operator
            mo = etree.SubElement(parent,"mo")
            mo.text = html.unescape(translatepname(self.get_name()))

            #third output the xml for child1
            mrow2 = etree.SubElement(parent, "mrow")
            self.get_nextchild().outputpresxml(mrow2)

    def outputnextpresxml(self, parent, prevop):
        #make the lhs child
        self.get_child().outputpresxml(parent)
        #check the rhs child
        if self.get_nextchild().get_name().strip() == prevop :
            self.get_nextchild().outputnextpresxml(parent, prevop)

        else:
            # make last rhs child
            self.get_nextchild().outputpresxml(parent)

    def outputcontxml(self,parent):
        #some constant and symbol elements are represented as operator
        #nodes however they don't require wrapping in "apply" elements
        #i expect that they don't have children
        name = translatecname(self.get_name().strip())
        #below are the elements which dont' require wrapping in apply
        constantsandsymbols = [ "emptyset", "eulergamma", "exponentiale","false",
                               "imaginaryi", "infinity", "notanumber","pi","true"]
                              # "reals", "complexes", "integers", "naturalnumbers","primes","rationals"]
        if name in constantsandsymbols:
            #just output the operator
            op = etree.SubElement(parent, name)
        elif name == "separator":
            #just output the children
            self.get_child().outputcontxml(parent)
            try:
                #if next child is the same operator as the current element, just output ITS first child
                if self.get_nextchild().get_name().strip() == self.get_name().strip():
                    self.get_nextchild().outputnextcontxml(parent, self.get_name().strip())
                else:
                    self.get_nextchild().outputcontxml(parent)
            except AttributeError:
                pass

        else:
            apply = etree.SubElement(parent, "apply")
            print(self.get_name())
            op = etree.SubElement(apply, name)
            self.get_child().outputcontxml(apply)

            try:
                if self.get_nextchild().get_name().strip() == self.get_name().strip():
                    self.get_nextchild().outputnextcontxml(apply, self.get_name().strip())
                else:
                    self.get_nextchild().outputcontxml(apply)
            except AttributeError:
                pass


    def outputnextcontxml(self, parent, prevop):
        #make the lhs child
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
        # output the xml for only child if one exists
        try:
            self.get_child().outputpresxml(mrow)
        except AttributeError:
            pass
        moclose = etree.SubElement( mrow, "mo")
        moclose.text = html.unescape(self.get_closebrac())

    def outputcontxml(self,parent):
        #brackets dont need to be explicitly made for content ml;
        # theyre mostly decided on by the parser in the browser?
        #if not an interval, 'skip over' brackets? ie don't use the braclets for info but not in the output
        #what about function applications?... if it is required that the invisible function
        #application operator is used this can be handled relatively easily
        '''fine to skip over the brackets if the first and only child is not a separator
         as this should mean it is not an interval, list, set?'''
        openbracket = self.get_openbrac().strip()
        closebracket = self.get_closebrac().strip()

        if openbracket in ["&#8970;","⌊"] and closebracket in ["&#8971;", "⌋"]:
            #logic for the floor function
            apply = etree.SubElement(parent,"apply")
            floor = etree.SubElement(apply,"floor")
            if self.get_child() != None:
                #output the first child if one exists
                self.get_child().outputcontxml(apply)

        elif openbracket == "|" and closebracket == "|":
            #logic for the floor function
            apply = etree.SubElement(parent,"apply")
            floor = etree.SubElement(apply,"abs")
            if self.get_child() != None:
                #output the first child if one exists
                self.get_child().outputcontxml(apply)

        elif self.get_attributes().get("set") == "true" or (openbracket == "{" and closebracket == "}"):
            #this is the beginning of a tree representing a list
            #output list tag
            element = etree.SubElement(parent, "set")
            #output child
            if self.get_child() != None:
                #output the first child if one exists
                self.get_child().outputcontxml(element)

        else:
            answer = input("Are these brackets" + openbracket + closebracket + "best described"
                                                                             " as 1, 2 or 3?"" \n1) An interval \n2) A list\n"
                                                                             "3) Neither\nPlease enter the correct corresponding"
                                                                             " number: ")
            if self.get_attributes().get("list") == "true" or answer =="2":
                # this is the beginning of a tree representing a list
                # output list tag
                list = etree.SubElement(parent, "list")
                # output child
                if self.get_child() != None:
                    # output the first child if one exists
                    self.get_child().outputcontxml(list)
            elif answer == "1":
                # output interval tag
                intervalbrackets = openbracket + closebracket
                closuretypedict = {
                    "[]": "closed",
                    "(]":"open-closed",
                    "[)":"closed-open",
                    "()":"open"
                }
                list = etree.SubElement(parent, "interval", closure= closuretypedict.get(intervalbrackets))
                # output child
                if self.get_child() != None:
                    # output the first child if one exists
                    self.get_child().outputcontxml(list)
            elif self.get_child().get_attributes().get("separator") != "true" or answer == "3":
                # eg mfenced and other instances where brackets don't need to be kept
                self.get_child().outputcontxml(parent)


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
        try:
            interval = etree.SubElement(apply, "interval", closure=self.get_attributes().get("closure"))
        except TypeError:
            #closed is the default type of closure
            interval = etree.SubElement(apply, "interval", closure="closed")
        self.get_child().get_child().outputcontxml(apply)
        self.get_child().get_nextchild().outputcontxml(apply)

'''HERE''''''''''''''''''''''''''''''''''''''''''''''''';'''''
class NumberSet(Node):
    def __init__(self, name, attributes):
        super().__init__(attributes)
        self.name = name

    def get_name(self):
        return self.name

    def outputpresxml(self, parent):
        # output the xml for this element
        mi = etree.SubElement(parent, "mi", mathvariant = self.get_attributes().get("mathvariant") )
        mi.text = html.unescape(translatepname(self.get_name()))

    def outputcontxml(self, parent):
        # output the xml for this element
        op = etree.SubElement(parent, translatecname(self.get_name().strip()))


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
    #need this??

    def outputpresxml(self, parent):
        # output the xml for this element
        mi = etree.SubElement(parent, "mi")
        mi.text = html.unescape(self.get_name())

    def outputcontxml(self,parent):
        # output the xml for this element
        if self.get_name() in ["true", "false", "NaN", "&#8709;", "∅", "γ","&#947;","&#8734;" ,"∞"]: #&#8709; is empty set, &#960; is pi
            #these are elements represented in pres ml as identifiers but act like operators in cont ml
            op = etree.SubElement(parent, translatecname(self.get_name()))
        elif self.get_name().strip() in ["e","ln","i"]:
            answer = input("\"" +self.get_name() + "\" has been found. Does this identifier represent " +
                           translatecname(self.get_name()) + "? \ny/n:" )
            if answer == "y":
                op = etree.SubElement(parent, translatecname(self.get_name()))
            else:
                ci = etree.SubElement(parent, "ci")
                ci.text = self.get_name()
        else:
            ci = etree.SubElement(parent, "ci")
            ci.text = self.get_name()