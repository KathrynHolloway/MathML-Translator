from lxml import etree
from nodes import *

def docparse(file_location):

    # read in the contentML from file
    # produces an ElementTree
    parser = etree.XMLParser(load_dtd=True, no_network=False)
    doc = etree.parse(file_location, parser=parser)

    # this gets the xml version from the doc - doc.docinfo.xml_version
    # and the doc type doc.docinfo.doctype

    doc.docinfo.public_id = '-//W3C//ENTITIES HTML MathML Set//EN//XML'
    doc.docinfo.system_url = 'http://www.w3.org/2003/entities/2007/htmlmathml-f.ent'

    root = doc.getroot()

    print(get_tag(root), root.attrib, root.text)
    for child in root:
        print_child(child)
        get_children(child)


def get_tag(element):
    if "www." in element.tag:
        return element.tag[element.tag.index("}") + 1:]
    else:
        return element.tag
def get_children(child): #m this is for printing and visualising code
    for i in child:
        print_child(i)
        get_children(i)

def child_list(element):
    # gets a list of an elements children for use in check_node, excluding first to represent siblings
    list = []
    for child in element:
        list.append(child)
    if len(list)== 0:
        return list
    else:
        return list[1:]

def print_child(child):
    print(get_tag(child), child.attrib, child.text ,get_tag(child.getparent()))

def make_tree(file_location): #parses the file and converts to internal tree structure
    parser = etree.XMLParser(load_dtd=True, no_network=False)
    doc = etree.parse(file_location, parser=parser)
    #doc.docinfo.public_id = '-//W3C//ENTITIES HTML MathML Set//EN//XML'
    #doc.docinfo.system_url = 'http://www.w3.org/2003/entities/2007/htmlmathml-f.ent'

    root = doc.getroot()

    '''temporary pres/cont distinction'''
    tree  = check_pnode(root, [])
    # tree  = check_cnode(root, [])
    # differenetiate between pres tree and cont tree based on command line input
    '''todo'''

    return tree

'''Parsing presentation ML into the internal tree structure''' '''BEGINNING'''

def check_pnode(element, siblings):
    ignore = ["math", "mrow"]
    consider = ["mfrac", "msqrt", "msup","mfenced"]
    leaf = ["mn","mi"]
    tag = get_tag(element)

    #the element has no siblings so all we need to check is the current element
    if siblings == []:
        #can this element be ignored? if so move onto its children
        if tag in ignore:
            '''may need to add consideration for no children in future'''
            return check_pnode(element[0], child_list(element) )
        #is the curent element one we must consider?
        if tag in consider:
            '''will need to change when other tags get included'''
            #currently only does mfrac
            if tag == "mfrac":
                return make2childopnode( element ,siblings, "/" )
            if tag == "msup":
                return make2childopnode(element ,siblings, "power" )
            if tag == "msqrt":
                return make1childopnode(element ,siblings, "sqrt" )
            



        #is the current element a leaf?
        if tag in leaf:
            return leafnode(tag, element,siblings, element.text)

    #the current element has only one sibling
    if len(siblings) == 1:
        if tag == "mo":
            return opfirst(element,siblings, element.text)
        if tag in leaf:
            return leafnode(tag, element,siblings, element.text)

        # is the curent element one we must consider?
        if tag in consider:
            '''will need to change when other tags get included'''
            # currently only does mfrac
            if tag == "mfrac":
                return make2childopnode( element, siblings, "/")
            if tag == "msup":
                return make2childopnode(element, siblings, "power")
            if tag == "msqrt":
                return make1childopnode(element, siblings, "sqrt")
        #necessary?
        if tag in ignore:
            return check_pnode(element[0], child_list(element) )
        else:
            print( "something unexpected happened, code needs additions!" + tag)

    #len(siblings) >1  ie min of 3 tags to consider incl. the current element
    # consider the first two
    '''i expect that either the element or its first sibling will be an operator'''
    if len(siblings)>1:
        if tag == "mo": # operator is first, things get complex...
            #element is an operator and so is the sibling[1]
            #ie op elmnt op etc

            # is a bracket
            if element.text.strip() in ["(", "[", "{"]:
                #find closing bracket
                bracket2loc = find_other_bracket(siblings)

                #check if there is an operator after the closing bracket
                try:
                    next_sib = siblings[bracket2loc +1]
                    #if this exists it should be an operator 
                    if get_tag(next_sib) == "mo":
                        return make_bracket_node("opafter", element, siblings, bracket2loc)
                except IndexError:
                    print("location: except")
                    return make_bracket_node("justbrackets", element, siblings, bracket2loc)

            else: #not a bracket
                if get_tag(siblings[1]) == "mo":
                    return opthird( element, siblings, siblings[1].text)

        elif get_tag(siblings[0]) == "mo": # operator is second
            # check if the operator is a function application, it require different tree structure
            if element.text.strip() in ["sin", "cos" , "tan"]:
                #this assumes that a function application is applied to the sin, cos etc and its contents
                return opfirst(element, siblings[1:], element.text.strip())
            else:
                return opsecond(element,siblings, siblings[0].text)
        else:
            print("got stuck in multiple sibings logic")

def find_other_bracket(siblings):
    bracket2loc = 0
    i = 0
    while (i < len(siblings)):
        # print(siblings[i].text)
        if get_tag(siblings[i]) == "mo":
            if siblings[i].text.strip() in [")", "]", "}"]:
                break
        bracket2loc += 1
        i += 1
    return bracket2loc

def make2childopnode(element, siblings, name):
    #for nodes such as power, fractions etc which always have 2 children
    print("making: " + name)
    return Operator(name, check_pnode(element[0], []), check_pnode(element[1], []), element.attrib)

def make1childopnode(element, siblings, name):
    print("making: " + name)
    #sqrt
    # do they not have siblings always?
    return Operator(name, check_pnode(element[0], child_list(element)), None, element.attrib)

def opfirst(element, siblings, name):
    # op was first child
    if len(siblings) == 1:
        newsibs = []
    if len(siblings) > 1:
        newsibs = siblings[1:]
    print("making 1op: " + name)
    # do they always not have siblings ?
    # print("type", Operator(name, check_pnode(siblings[0], newsibs), None, element.attrib).get_name())
    return Operator(name, check_pnode(siblings[0], newsibs), None, element.attrib)

def opsecond(element, siblings, name):
    # the operator was first sibling, make and remove
    # can only currently get here if the current element has at least 2 siblings
    if len(siblings) == 2:
        newsibs = []
    else:  # ie len sibs > 2
        newsibs = siblings[2:]
    print("making 2op: " + name)
    return Operator(name, check_pnode(element, []), check_pnode(siblings[1], newsibs), siblings[0].attrib)

def opthird(element, siblings, name):
    print("making 3op: " + name)
    return Operator(name, check_pnode(element, siblings[:1]), check_for_psiblings(siblings[2:]), siblings[1].attrib)
    # return Operator(name, make_pnode("mi", siblings[0], [], siblings[0].text), check_for_psiblings(siblings[2:]),
    #                 siblings[1].attrib)

def leafnode(type, element, siblings, name):
       if type == "mn":
        # make a value node
        sibling = check_for_psiblings(siblings)
        print("making mn: " + name)
        return Value(name, sibling, element.attrib)  # keeps any attribs from mn
       if type == "mi":
           #make identifier node
           sibling = check_for_psiblings(siblings)
           print("making mi: " + name)
           return Identifier(name, sibling, element.attrib)  # keeps any attribs from mi
       else:
           pass

#made this for help with more complex bracket scenarios
def make_bracket_node(type, element, siblings, bracket2loc ):
    #note, bracket1loc is element
    if type == "opafter":
        #the brackets
        #the operator after the brackets
        print("making op after bracket: " + siblings[bracket2loc +1].text) #correct

        return Operator(siblings[bracket2loc +1].text, check_pnode(element, siblings[:bracket2loc +1]), check_for_psiblings(siblings[bracket2loc +2:]), siblings[bracket2loc +1].attrib)

    if type == "justbrackets":
        print("making justbrackets: " + element.text.strip() + siblings[bracket2loc].text.strip())

        return Brackets(element.text.strip(), siblings[bracket2loc].text.strip(), check_for_psiblings(siblings[:bracket2loc]), element.attrib)


    else:
        print("Tag = " + get_tag(element) + "needs logic implementing")


#helper method, considers how many siblings there are and uses that to return what the sibling of a presentation node should be
def check_for_psiblings(siblings):
    # returns value for siblings
    if siblings == []:
        sibling = None
    if len(siblings) == 1:
        sibling = check_pnode(siblings[0], [])
    if len(siblings) > 1:
        sibling = check_pnode(siblings[0], siblings[1:])
    return sibling

'''END OF PRES ML'''

'''Parsing content ML into the internal tree structure'''

def check_cnode(element, siblings):
    ignore = ["math" ,"apply", "reln"]
    consider = ["plus", "minus", "times", "divide", "eq" ,"sin", "cos", "tan","root","power", "factorial"]
    consider_node_name = ["+", "-", "&#8290;", "/", "=", "sin", "cos", "tan","sqrt","power", "!"]
    leaf = ["cn", "ci"]

    # the element is the only xml node available for consideration
    if len(siblings) == 0:
        if get_tag(element) in ignore:
            return check_cnode(element[0], child_list(element))
        if get_tag(element) in leaf:
            if get_tag(element) == leaf[0]: #cn
                return make_cnode("cn", element, siblings, element.text)
            if get_tag(element) == leaf[1]:
                return make_cnode("ci", element, siblings, element.text)
        #won't be in consider, can't apply an operator to nothing?

    #the element and one sibling xml node are what is available for consideration
    if len(siblings) == 1:
        if get_tag(element) in ignore:
            print("add some logic here")
        if get_tag(element) in consider:
            i = 0
            while i <= len(consider):
                if get_tag(element) == consider[i]:
                    return make_cnode("operator", element, siblings, consider_node_name[i])
                i += 1
    if len(siblings) >1:
        if get_tag(element) in consider:
            i=0
            while i <= len(consider):
                if get_tag(element) == consider[i]:
                    return make_cnode("operator", element, siblings, consider_node_name[i])
                i+=1


        else:
            print("len(siblings) >1 logic needs adding")

    else:
        print("logic missing, help!")




def make_cnode(type, element, siblings, name):
    #Value nodes
    if type == "cn":
        print("making cn: " + name)
        return Value(name, None, element.attrib)
    #Identifier nodes
    if type == "ci":
        print("making ci: " + name)
        return Identifier(name, None, element.attrib)
    if type == "operator":
        print("making op: " + name)
        return Operator(name, check_cnode(siblings[0], []), check_op_siblingsc(element, siblings), element.attrib  )

'''helper method for checking what the sibling for an operator node'''
def check_op_siblingsc(element, siblings):
    # returns value for siblings
    if len(siblings) == 1:
        opsibling = None
    if len(siblings) == 2:
        opsibling = check_cnode(siblings[1], [])
    if len(siblings) > 2:
        opsibling = check_cnode(element, siblings[1:])
    return opsibling



'''below didn't make a simple enough internal tree structure, needs to be more math focused, remove the XML'''

# def make_nodes(element, siblings): # creates individual nodes but calls itself for those nodes with children/siblings which are themselves nodes
#     attributes = element.attrib
#     try:
#         child = get_tag(element[0])
#         child = make_nodes(element[0],child_list(element))
#     except IndexError:
#         try:
#             text = element.text
#             child =  Value(text, None, None, None) # 'None' for sibling makes the assumption that leafs cannot have siblings, children or attribs
#         except AttributeError:
#             child = None
#     if siblings == []:
#         sibling = None
#     elif len(siblings)== 1:
#         sibling = make_nodes(siblings[0],[])
#     else:
#         sibling = make_nodes(siblings[0], siblings[1:])
#
#     return Value(get_tag(element), child, sibling, attributes )

