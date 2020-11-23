from lxml import etree
from src.optimisepresml import optimise
import src.nodes


'''for now, print the xml as a string instead of writing to an actual file?'''

def presxmlout(tree, output_file_loc):
    '''want to walk the tree and make my personal structure back into an etree
    but before that, check for any issues with invisible times'''

    invisibletimescheck(tree)
    
    # root = etree.Element(tree.get_name())
    # makechildren(tree, root)
    root = etree.Element("math", xmlns="http://www.w3.org/1998/Math/MathML")
    mrow = etree.SubElement(root, "mrow")

    #make the other nodes from the internal tree structure

    tree.outputpresxml(mrow)

    optimisedtree = optimise(root)

    # write_to_file(str(etree.tostring(root)),output_file_loc)
    write_to_file(str(etree.tostring(optimisedtree)),output_file_loc)

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
        "&#8800;":"neq",
        "≠":"neq",
        "+": "plus",
        "-": "minus",
        "&#8290;":"times", #invisible times
        "⁢":"times", #invisible times
        "/":"divide",
        "!":"factorial",
        "sqrt": "root",
        "&#x2243;":"approx",
        "≃":"approx",
        "&#8801;":"equivalent",
        "≡":"equivalent",
        "&#x2265;": "geq",
        "&&#8805;": "geq",
        "≥": "geq",
        "&#x2264;": "leq",
        "&#8804;": "leq",
        "≤": "leq",
        "&#x3e;": "gt", #gt symbol can be expressed multiple ways in pres ml
        "&gt;": "gt",
        ">": "gt",
        "±":"plus",
        "&#x3c;" : "lt",
        "&lt;" : "lt",
        "<" : "lt",
        "&#172;":"not",
        "¬":"not",
        "&#xFF5C;":"factorof",
        "power": "power",
        "sin": "sin",
        "cos": "cos",
        "tan":"tan",
        "&#x2208;": "in",
        "&#8712;": "in",
        "∈": "in",
        "complexes": "complexes",
        "integers": "integers",
        "emptyset": "emptyset",
        "&#8709;": "emptyset",
        "∅": "emptyset",
        "eulergamma": "eulergamma",
        "γ": "eulergamma",
        "&#947;": "eulergamma",
        "ln": "ln",
        "exponentiale": "exponentiale",
        "e": "exponentiale",
        "and": "and",
        "∧": "and",
        "&#8743;": "and",
        "false": "false",
        "imaginaryi": "imaginaryi",
        "i": "imaginaryi",
        "infinity": "infinity",
        "∞": "infinity",
        "&#8734;": "infinity",
        "naturalnumbers": "naturalnumbers",
        "notanumber": "notanumber",
        "pi": "pi",
        "&#960;": "pi",
        "π": "pi",
        "primes": "primes",
        "rationals": "rationals",
        "reals": "reals",
        "or": "or",
        "&#8744;": "or",
        "∨": "or",
        "true":"true",
        "abs": "abs",
        "card": "card",
        "rem": "rem",
        "mod": "rem",
        "gcd": "gcd",
        "lcm": "lcm",
        "floor":"floor",
        "xor": "xor",
        "implies": "implies",
        "&#8658;": "implies",
        "⇒": "implies",
        "arg": "arg",
        ",":"separator",
        "NaN" :"notanumber",
        "&#8289;":"fnapplication",
        "⁡":"fnapplication",
        "cartesianproduct": "cartesianproduct",
        "vectorproduct": "vectorproduct",
        "×": "ambiguous", #multiplication sign
        "&#xd7;": "ambiguous",
        "&#215;": "ambiguous",

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
        "abs": ["|","|"],
        "card": ["|","|"],
        "rem": "mod",
        "gcd": ["gcd","(",")",","], #prefix, open, close, separators
        "lcm": ["lcm","(",")",","],
        "arg": ["arg","(",")",""],
        "floor": ["&#x230a;","&#x230b;"],
        "xor": "xor",
        "implies": "&#x21d2;", #rightwards double arrow
        "cartesianproduct": "&#xd7;", #multiplication sign
        "vectorproduct": "&#xd7;" #multiplication sign

    }
    separators = [":", ";", ",","|"]
    if presnamedict.get(nodename)!=None:
        newname = presnamedict.get(nodename)
    elif nodename in ["+", "-", "=", "!", "&#8290;"] or separators: #these don't change
        newname = nodename
    elif presnamedict.get(nodename) == None:
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


def invisibletimescheck(element):
    '''note indexing shouldn't be an issue as times is a binary operation.
    caution necessary when operation isn't times'''
    #checks for any issues with multiplication as invisible times is used as a default when parsing times
    if type(element) is nodes.Operator and element.get_name() == "&#8290;":
        if type(element.get_child()) is nodes.Value and type(element.get_nextchild()) is nodes.Value: #if both children of times are numbers, "x" necessary
            element.set_name("&#xd7;")
        elif type(element.get_child()) is nodes.Value and element.get_nextchild().get_name() == "&#8290;" \
                and type(element.get_nextchild().get_child()) is nodes.Value:
            #covers multiplication of more than two numbers together
            element.set_name("&#xd7;")
            invisibletimescheck(element.get_nextchild())
        else:
            invisibletimescheck(element.get_nextchild())
    else:
        '''could be none times operator or leaf node'''
        try:
            invisibletimescheck(element.get_child())
            invisibletimescheck(element.get_nextchild())
        except:
            pass

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

