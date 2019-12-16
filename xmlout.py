from lxml import etree

'''for now, print the xml as a string instead of writing to an actual file?'''

def presxmlout(tree, output_file_loc):
    # with open(output_file_loc, 'w') as output_file:
    #     output_file.write('some info here. great')
    '''above: if the file exists it writes to (and over) that file
             should create a file if one with that name doesn't exist, then write'''
    '''next: want to walk the tree and make my personal structure back into and etree'''
    
    # root = etree.Element(tree.get_name())
    # makechildren(tree, root)
    root = etree.Element("math", xmlns="http://www.w3.org/1998/Math/MathML")
    mrow = etree.SubElement(root, "mrow")

    #make the other nodes from the internal tree structure

    tree.outputpresxml(mrow)

    write_to_file(str(etree.tostring(root)),output_file_loc)

    # return etree.tostring(root)


def contxmlout(tree, output_file_loc):
    # with open(output_file_loc , 'w') as output_file:
    #     output_file.write('some info here. great')
    '''above: if the file exists it writes to (and over) that file
             should create a file if one with that name doesn't exist, then write'''
    '''next: want to walk the tree and make my personal structure back into and etree'''

    root = etree.Element("math", xmlns="http://www.w3.org/1998/Math/MathML")

    # make the other nodes from the internal tree structure

    tree.outputcontxml(root)

    write_to_file(str(etree.tostring(root)), output_file_loc)

    # return etree.tostring(root)

''' +, - , etc aren't valid content tag names so they need changing'''
def translatecname(nodename):
    #this removes any unnecessary whitespace which would prevent this method from working correctly
    nodename = nodename.strip()
    contnamedict = {
        "=" : "eq",
        "&#x2260;":"neq",
        "+": "plus",
        "-": "minus",
        "&#8290;":"times",
        "/":"divide",
        "!":"factorial",
        "sqrt": "root",
        "&#x2243;":"approx",
        "&#8801;":"equivalent",
        "&#x2265;": "geq",
        "&#x2264;": "leq",
        "&#x3e;": "gt",
        "&#x3c;" : "lt",
        "&#172;":"not",
        "&#xFF5C;":"factorof",
        "power": "power",
        "sin": "sin",
        "cos": "cos",
        "tan":"tan",
        "&#x2208;": "in",
        "complexes": "complexes",
        "integers": "integers",
        "emptyset": "emptyset",
        "eulergamma": "eulergamma",
        "ln": "ln",
        "exponentiale": "exponentiale",
        "and": "and",
        "false": "false",
        "imaginaryi": "imaginaryi",
        "infinity": "infinity",
        "naturalnumbers": "naturalnumbers",
        "notanumber": "notanumber",
        "pi": "pi",
        "primes": "primes",
        "rationals": "rationals",
        "reals": "reals",
        "or": "or",
        "true":"true",
        "abs": "abs",
        "rem": "rem",
        "gcd": "gcd",
        "lcm": "lcm"

    }
    newname = contnamedict.get(nodename)
    return newname

def translatepname(nodename):
    nodename = nodename.strip()
    presnamedict = {
        "sqrt": "msqrt",
        "/": "mfrac",
        "divide": "mfrac",
        "power": "msup",
        "complexes" : "C",
        "integers": "Z",
        "emptyset": "&#x2205",
        "eulergamma": "&#x3b3;",
        "exponentiale": "e",
        "false": "false",
        "and": "&#x2227;",
        "imaginaryi": "i",
        "infinity": "&#x221e;",
        "naturalnumbers": "N",
        "notanumber": "NaN",
        "pi": "&#x3c0;",
        "primes": "P",
        "rationals": "Q",
        "reals": "R",
        "or": "&#x2228;",
        "abs": "||",
        "rem": "mod",
        "gcd": ["gcd","(",")",","], #prefix, open, close, separators
        "lcm": ["lcm","(",")",","]
    }
    separators = [":", ";", ",","|"]
    if presnamedict.get(nodename)!=None:
        newname = presnamedict.get(nodename)
    elif nodename in ["+", "-", "=", "!", "&#8290;"] or separators: #these don't change
        newname = nodename
    else:
        print(nodename, "Hasn't been implemented yet")
    return newname

def write_to_file(treestring, output_file_loc):
    with open(str(output_file_loc), "w") as output_file:
        output_file.write("<!DOCTYPE math PUBLIC "+ "\"-//W3C//DTD MathML 3.0//EN\"" +" \"http://www.w3.org/Math/DTD/mathml3/mathml3.dtd\"" +"> \n")
    with open(str(output_file_loc), 'a') as output_file:
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

