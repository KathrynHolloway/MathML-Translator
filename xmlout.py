from lxml import etree

'''for now, print the xml as a string instead of writing to an actual file?'''

def presxmlout(tree):
    # with open("output.xml", 'w') as output_file:
    #     output_file.write('some info here. great')
    '''above: if the file exists it writes to (and over) that file
             should create a file if one with that name doesn't exist, then write'''
    '''next: want to walk the tree and make my personal structure back into and etree'''
    
    # root = etree.Element(tree.get_name())
    # makechildren(tree, root)
    root = etree.Element("math")
    mrow = etree.SubElement(root, "mrow")

    #make the other nodes from the internal tree structure

    tree.outputpresxml(mrow)

    write_to_file(str(etree.tostring(root)))

    return etree.tostring(root)


def contxmlout(tree):
    # with open("output.xml", 'w') as output_file:
    #     output_file.write('some info here. great')
    '''above: if the file exists it writes to (and over) that file
             should create a file if one with that name doesn't exist, then write'''
    '''next: want to walk the tree and make my personal structure back into and etree'''

    root = etree.Element("math")

    # make the other nodes from the internal tree structure

    tree.outputcontxml(root)

    write_to_file(str(etree.tostring(root)))

    return etree.tostring(root)

''' +, - , etc aren't valid content tag names so they need changing'''
def translatename(nodename):
    if nodename == "=":
        newname = "eq"
    if nodename == "+":
        newname = "plus"
    if nodename == "-":
        newname = "minus"
    if nodename == "*":
        newname = "times"
    if nodename == "/":
        newname = "divide"
    if nodename == "!":
        newname = "factorial"
    if nodename == "sqrt":
        newname = "root"
    remain = ["power", "sin", "cos", "tan"]
    if nodename in remain:
        newname = nodename
    return newname

def write_to_file(treestring):
    with open("output.xml", "w") as output_file:
        output_file.write("<!DOCTYPE math PUBLIC "+ "\"-//W3C//DTD MathML 3.0//EN\"" +" \"http://www.w3.org/Math/DTD/mathml3/mathml3.dtd\"" +"> \n")
    with open("output.xml", 'a') as output_file:
        output_file.write(treestring[2:-1])
    '''above: if the file exists it writes to (and over) that file
             should create a file if one with that name doesn't exist, then write'''
    '''next: want to walk the tree and make my personal structure back into and etree'''


# def makechildren(treenodeparent, xmlparent):
#     #print(treenodeparent)
# 
#     child = treenodeparent.get_child()
#     while child != None:
#         # xmlparent.append(etree.Element(child.get_name()))
#         # parent = xmlparent.append(etree.Element(child.get_name()))
#         print(child.get_name())
#         try:
#             parent = etree.SubElement(xmlparent, child.get_name())
#             print(parent)
#             makechildren(child, parent)
#         except ValueError:
#             #parent = etree.SubElement(xmlparent, "OPERATOR")
#             '''it didn't like making operators into tags. 
#             also strip required for say, x'''
#             xmlparent.text = child.get_name()#.strip()
# 
# 
#         child = child.get_sibling()

