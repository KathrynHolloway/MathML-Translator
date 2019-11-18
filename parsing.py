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

    '''temporary pres/cont distinction'''
    # tree  = check_pnode(root, [])
    tree  = check_cnode(root, [])
    # differenetiate between pres tree and cont tree based on command line input
    '''todo'''

    return tree

'''Parsing presentation ML into the internal tree structure'''

def check_pnode(element, siblings):
    ignore = ["math", "mrow"]
    consider = ["mfrac", "msqrt", "msup"]
    leaf = ["mn","mi"]

    #the element has no siblings so all we need to check is the current element
    if siblings == []:
        #can this element be ignored? if so move onto its children
        if get_tag(element) in ignore:
            '''may need to add consideration for no children in future'''
            return check_pnode(element[0], child_list(element) )
        #is the curent element one we must consider?
        if get_tag(element) in consider:
            '''will need to change when other tags get included'''
            #currently only does mfrac
            if get_tag(element) == "mfrac":
                return make_pnode("2arynode" , element ,siblings, "frac" )
            if get_tag(element) == "msup":
                return make_pnode("2arynode" , element ,siblings, "power" )
            if get_tag(element) == "msqrt":
                return make_pnode("narynode" , element ,siblings, "sqrt" )


        #is the current element a leaf?
        if get_tag(element) in leaf:
            return make_pnode(get_tag(element), element,siblings, element.text)

    #the current element has only one sibling
    if len(siblings) == 1:
        if get_tag(element) == "mo":
            return make_pnode("1op", element,siblings, element.text)
        if get_tag(element) in leaf:
            return make_pnode(get_tag(element), element,siblings, element.text)

        # is the curent element one we must consider?
        if get_tag(element) in consider:
            '''will need to change when other tags get included'''
            # currently only does mfrac
            if get_tag(element) == "mfrac":
                return make_pnode("2arynode", element, siblings, "/")
            if get_tag(element) == "msup":
                return make_pnode("2arynode", element, siblings, "power")
            if get_tag(element) == "msqrt":
                return make_pnode("narynode", element, siblings, "sqrt")
        #necessary?
        if get_tag(element) in ignore:
            return check_pnode(element[0], child_list(element) )
        else:
            print( "something unexpected happened, code needs additions!" + get_tag(element))

    #len(siblings) >1  ie min of 3 tags to consider incl. the current element
    # consider the first two
    '''i expect that either the element or its first sibling will be an operator'''
    if len(siblings)>1:
        if get_tag(element) == "mo": # operator is first, things get complex...
            #element is an operator and so is the sibling[1]
            #ie op elmnt op etc
            bracket2loc = 0
            # is a bracket
            if element.text.strip() in ["(", "[", "{"]:
                #find closing bracket
                i=0
                while (i < len(siblings)):
                    print(siblings[i].text)
                    if get_tag(siblings[i]) =="mo":
                        if siblings[i].text.strip() in [")", "]", "}"]:
                            break
                    bracket2loc += 1
                    i+=1

                try:
                    next_sib = siblings[bracket2loc +1]
                    #if this exists it should be an operator 
                    if get_tag(next_sib) == "mo":
                        print("in try bracket clause, loc = " , bracket2loc)
                        make_bracket_node("opafter", element, siblings, bracket2loc)
                except IndexError:
                    print("location: except")
                    make_bracket_node("justbrackets", element, siblings, bracket2loc)

            else: #not a bracket
                if get_tag(siblings[1]) == "mo":
                    make_pnode("3op", element, siblings, siblings[1].text)


        elif get_tag(siblings[0]) == "mo": # operator is second
            return make_pnode("2op", element,siblings, siblings[0].text)
        else:
            print("got stuck in multiple sibings logic")



def make_pnode(type, element, siblings, name):
    '''This method will actually return the nodes that 'check_pnode' deems should be kept'''

    if type == "2arynode": # an operator that isnt "op" tag that always has 2 children eg sup, frac
        print("making: " + name)
        return Operator(name, check_pnode(element[0], []), check_pnode(element[1],[]) , element.attrib)

    if type == "narynode": # an operator that isnt "op" tag that may have 1 or 2 children eg sqrt, usually 1 though?
        print("making: " + name)
        #do they not have siblings always?
        return Operator(name, check_pnode(element[0], child_list(element)), None , element.attrib)

    '''COME BACK TO SQRT'''

    if type == "1op":
        # op was first child
        if len(siblings) == 1:
            newsibs = []
        if len(siblings)>1:
            newsibs = siblings[1:]
        print("making 1op: " + name)
        #do they always not have siblings ?
        return Operator(name, check_pnode(siblings[0],newsibs  ) , None,  element.attrib)
    if type == "2op":
        #the operator was second child, remove
        # can only currently get here if the current element has at least 2 siblings
        if len(siblings) == 2:
            newsibs = []
        else: # ie len sibs > 2
            newsibs = siblings[2:]
        print("making 2op: " + name)
        return Operator(name, check_pnode(element, []), check_pnode(siblings[1], newsibs), siblings[0].attrib)

    if type == "3op":
        print("making 3op: " + name)
        # return Operator(name, check_pnode(element, siblings[0]), check_for_psiblings(siblings[2:]), siblings[1].attrib)
        return Operator(name, make_pnode("mi", siblings[0], [], siblings[0].text), check_for_psiblings(siblings[2:]), siblings[1].attrib)

    #make a value node
    if type == "mn":
        sibling = check_for_psiblings(siblings)
        print("making mn: " + name)
        return Value(name, sibling, element.attrib)  # keeps any attribs from mn
    #make a value node
    if type == "mi":
        sibling = check_for_psiblings(siblings)
        print("making mi: " + name)
        return Identifier(name, sibling, element.attrib) # keeps any attribs from mi
    else:
        print("Tag = " + get_tag(element) + "needs logic implementing" )

#made this for help with more complex bracket scenarios
def make_bracket_node(type, element, siblings, bracket2loc ): #note, bracket1loc is element
    if type == "opafter":
        #the brackets
        # firstchild = Operator( element.text.strip() + siblings[bracket2loc].text.strip(), check_for_psiblings(siblings[:bracket2loc]),None, element.attrib)
        # secondchild = check_for_psiblings(siblings[bracket2loc+2:])
        #the operator after the brackets
        # print("op after bracket: ", siblings[bracket2loc +1].text)
        print("making op after: " + siblings[bracket2loc +1].text)
        return Operator(siblings[bracket2loc +1].text, check_pnode(element, siblings[:bracket2loc +1]), check_for_psiblings(siblings[bracket2loc +2:]), siblings[bracket2loc +1].attrib)
        # return Operator(siblings[bracket2loc +1].text, firstchild, secondchild, siblings[bracket2loc +1].attrib)

    if type == "justbrackets":
        print("brac loc : " , bracket2loc)
        print("making justbrackets: " + element.text.strip() + siblings[bracket2loc].text.strip())
        # return Operator(name, check_for_psiblings(siblings[:bracket2loc]), None, element.attrib)
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


'''Parsing content ML into the internal tree structure'''

def check_cnode(element, siblings):
    ignore = ["math" ,"apply", "reln"]
    consider = ["plus", "minus", "times", "divide", "eq" ,"sin", "cos", "tan"]
    consider_node_name = ["+", "-", "*", "/", "eq", "sin", "cos", "tan"]
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

