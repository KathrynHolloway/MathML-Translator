from lxml import etree
from nodes import Node

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

def child_list(element): # gets a lsit of an elements children for use in make_node, excluding first
    list = []
    for child in element:
        list.append(child)
    if len(list)== 0:
        # try:
        #     text = element.text
        #     list.append(text)
        #     return list
        # except AttributeError:
        #     return list
        return list
    else:
        return list[1:]

def print_child(child):
    print(get_tag(child), child.attrib, child.text ,get_tag(child.getparent()))

def make_tree(file_location): #parses the file and converts to internal tree structure # tested on presentation ML
    parser = etree.XMLParser(load_dtd=True, no_network=False)
    doc = etree.parse(file_location, parser=parser)
    #doc.docinfo.public_id = '-//W3C//ENTITIES HTML MathML Set//EN//XML'
    #doc.docinfo.system_url = 'http://www.w3.org/2003/entities/2007/htmlmathml-f.ent'

    root = doc.getroot()

    tree  = make_node(root, [])

    return tree
        #get_tag(root), root[0].tag, etree._Element.getnext(root))
    # print( tree.tag ,  tree.child, tree.sibling)
    # print(get_tag(root), root.attrib, root.text)
    # for child in root:
    #     print_child(child)
    #     get_children(child)
    #

def make_node(element, siblings): # creates individual nodes but calls itself for those nodes with children/siblings which are themselves nodes
    attributes = element.attrib
    try:
        child = get_tag(element[0])
        child = make_node(element[0],child_list(element))
    except IndexError:
        try:
            text = element.text
            child =  Node(text, None, None, None) # 'None' for sibling makes the assumption that leafs cannot have siblings, children or attribs
        except AttributeError:
            child = None
    if siblings == []:
        sibling = None
    elif len(siblings)== 1:
        sibling = make_node(siblings[0],[])
    else:
        sibling = make_node(siblings[0], siblings[1:])
        
    return Node(get_tag(element), child, sibling, attributes )