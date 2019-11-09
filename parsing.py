from lxml import etree
from nodes import *

def docparse(file_location):

    # read in the contentML from file
    # produces an ElementTree
    parser = etree.XMLParser(load_dtd=True, no_network=False)
    doc = etree.parse(file_location, parser=parser)

    #"quadformpres4.xml" use this xml doc for testing
    # this gets the xml version from the doc - doc.docinfo.xml_version
    # and the doc type doc.docinfo.doctype

    doc.docinfo.public_id = '-//W3C//ENTITIES HTML MathML Set//EN//XML'
    doc.docinfo.system_url = 'http://www.w3.org/2003/entities/2007/htmlmathml-f.ent'

    root = doc.getroot()

    print(get_tag(root), root.attrib, root.text)
    for child in root:
        print_child(child)
        get_children(child)
    


# accessing the children of the root
# for child in root:
#     print(child.tag, child.attrib, child.text)


# The siblings (or neighbours) of an element are accessed as next and previous elements

# print(root[0] is root[1].getprevious())
# print( root[1] is root[0].getnext())

# for child in root:
#    print(child.tag,'child0')
#
#    for i in child:
#        print(i.tag,'child1')
#        for j in i:
#            print(j.tag,'child2')
#            for k in j:
#                print(k.tag, 'child3')

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

    tree  = check_node(root, []) # differenetiate between pres tree and cont tree based on command line input
    '''todo'''

    return tree
        #get_tag(root), root[0].tag, etree._Element.getnext(root))
    # print( tree.tag ,  tree.child, tree.sibling)
    # print(get_tag(root), root.attrib, root.text)
    # for child in root:
    #     print_child(child)
    #     get_children(child)
    #

def check_node(element, siblings):
    ignore = ["math", "mrow"]
    consider = ["mfrac"]
    leaf = ["mn","mi"]

    #the element has no siblings so all we need to check is the current element
    if siblings == []:
        #can this element be ignored? if so move onto its children
        if get_tag(element) in ignore:
            '''may need to add consideration for no children in future'''
            return check_node(element[0], child_list(element) )
        #is the cuurent element one we must not make a node of, but consider?
        if get_tag(element) in consider:
            '''will need to change when other tags get included'''
            #currently only does mfrac
            return make_node("frac_op" , element ,siblings, "/" )
        #is the current element a leaf?
        if get_tag(element) in leaf:
            return make_node(get_tag(element), element,siblings, element.text)

    #the current element has only one sibling
    if len(siblings) == 1:
        if get_tag(element) == "mo":
            return make_node("op", element,siblings, element.text)
        if get_tag(element) in leaf:
            return make_node(get_tag(element), element,siblings, element.text)

        else:
            print( "something unexpected happened, code needs additions!")
    '''add for when operstor added and has two mn children for example 
    ie neither the element or the single sibling is an operator '''

    #len(siblings) >1
    # consider the first two
    '''i expect that either the element or its first sibling will be an operator'''
    if len(siblings)>1:
        if get_tag(element) == "mo":
            return make_node("op", element,siblings, element.text)
        if get_tag(siblings[0]) == "mo":
            return make_node("op", element,siblings, siblings[0].text)#get_tag(siblings[0]))



def make_node(type, element, siblings, name):
    '''This method will actually return the nodes that 'check_node' deems should be kept'''
    if type == "frac_op":
        return Operator(name, check_node(element[0], child_list(element)) , element.attrib)

    if type == "op":
        return Operator(name, check_node(element, siblings[1:]) , siblings[0].attrib)
    
    #make a value node
    if type == "mn":
        if siblings == []:
            sibling = None
        if len(siblings) == 1:
            sibling = check_node(siblings[0], [])
        if len(siblings)>1:
            sibling = check_node(siblings[0], siblings[1:])
        return Value(name, sibling, element.attrib)  # keeps any attribs from mn
        # if type == "mn":
        #     return Value(name, sibling , element.attrib) # keeps any attribs from mn
        # if type == "mi":
        #     return Identifier(name, sibling, element.attrib) # keeeps any attribs from mi
    #make a value node
    if type == "mi":
        if siblings == []:
            sibling = None
        if len(siblings) == 1:
            sibling = check_node(siblings[0], [])
        if len(siblings)>1:
            sibling = check_node(siblings[0], siblings[1:])
        return Identifier(name, sibling, element.attrib) # keeeps any attribs from mi
    else:
        print("Tag = " + get_tag(element) + "needs logic implementing" )

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