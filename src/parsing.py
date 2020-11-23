from lxml import etree
from src.nodes import *
import html
#
# def docparse(file_location):
#
#     # read in the contentML from file
#     # produces an ElementTree
#     parser = etree.XMLParser(load_dtd=True, no_network=False)
#     doc = etree.parse(file_location, parser=parser)
#
#     # this gets the xml version from the doc - doc.docinfo.xml_version
#     # and the doc type doc.docinfo.doctype
#
#     doc.docinfo.public_id = '-//W3C//ENTITIES HTML MathML Set//EN//XML'
#     doc.docinfo.system_url = 'http://www.w3.org/2003/entities/2007/htmlmathml-f.ent'
#
#     root = doc.getroot()
#
#     print(get_tag(root), root.attrib, root.text)
#     for child in root:
#         print_child(child)
#         get_children(child)


def get_tag(element):
    if "www." in element.tag:
        return element.tag[element.tag.index("}") + 1:]
    else:
        return element.tag

def child_list(element):
    # gets a list of an elements children for use in check_node, excluding first to represent siblings
    list = []
    for child in element:
        list.append(child)
    if len(list)== 0:
        return list
    else:
        return list[1:]

# def print_child(child):
#     print(get_tag(child), child.attrib, child.text ,get_tag(child.getparent()))

def doc_parse(input_file_location):
    parser = etree.XMLParser(load_dtd=True, no_network=False)
    parsed_doc = etree.parse(input_file_location, parser=parser)
    # doc.docinfo.public_id = '-//W3C//ENTITIES HTML MathML Set//EN//XML'
    # doc.docinfo.system_url = 'http://www.w3.org/2003/entities/2007/htmlmathml-f.ent'
    return parsed_doc

def make_contentml_tree(parsed_doc): #takes parsed content ml file and converts to internal tree structure
    root = parsed_doc.getroot()
    tree  = check_cnode(root, [])

    return tree

def make_presml_tree(parsed_doc):  # takes parsed content ml file and converts to internal tree structure
    root = parsed_doc.getroot()
    tree = check_pnode(root, [])

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
            if tag == "mfenced":
                return make_bracket_node(tag,element, siblings, None)

        #is the current element a leaf?
        if tag in leaf:
            return leafnode(tag, element,siblings, element.text)

    #the current element has only one sibling
    if len(siblings) == 1:
        if tag == "mo":
            if element.text.strip() in ["(", "[", "{","&#8970;","⌊"] and siblings[0].text.strip() in [")", "]", "}","&#8971;","⌋"]:
                return make_bracket_node("justbrackets",element, siblings, 0)
            else:
                return opfirst(element,siblings, element.text)
        elif get_tag(siblings[0]) == "mo":
            return opsecond(element,siblings, siblings[0].text)
            #example case is factorial (!)
        elif tag in leaf:
            return leafnode(tag, element,siblings, element.text)

        # is the curent element one we must consider?
        elif tag in consider:
            '''will need to change when other tags get included'''
            # currently only does mfrac
            if tag == "mfrac":
                return make2childopnode( element, siblings, "/")
            if tag == "msup":
                return make2childopnode(element, siblings, "power")
            if tag == "msqrt":
                return make1childopnode(element, siblings, "sqrt")
        #necessary?
        elif tag in ignore:
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
            if element.text.strip() in ["(", "[", "{","&#8970;","⌊"]:
                #find closing bracket
                bracket2loc = find_other_bracket(siblings)

                #check if there is an operator after the closing bracket
                try:
                    next_sib = siblings[bracket2loc +1]
                    #if this exists it should be an operator 
                    if get_tag(next_sib) == "mo":
                        return make_bracket_node("opafter", element, siblings, bracket2loc)
                except IndexError:
                    # print("location: except")
                    return make_bracket_node("justbrackets", element, siblings, bracket2loc)

            else: #not a bracket
                if get_tag(siblings[1]) == "mo":
                    return opthird( element, siblings, siblings[1].text)

        elif get_tag(siblings[0]) == "mo": # operator is second
            # check if the operator is a function application, it require different tree structure
            if element.text.strip() in ["sin", "cos" , "tan", "ln"]:
                #this assumes that a function application is applied to the sin, cos etc and its contents
                return opfirst(element, siblings[1:], element.text.strip())
            else:
                return opsecond(element,siblings, siblings[0].text)
        else:
            print("got stuck in multiple sibings logic")

def find_other_bracket(siblings):
    bracket2loc = 0
    siblingnumber = 0
    incompletebrackets = 0
    while (siblingnumber < len(siblings)):
        # print(siblings[i].text)
        if get_tag(siblings[siblingnumber]) == "mo":
            if siblings[siblingnumber].text.strip() in ["(", "[", "{","&#8970;","⌊"]:
                incompletebrackets += 1
            if siblings[siblingnumber].text.strip() in [")", "]", "}","&#8971;", "⌋"]:
                if incompletebrackets == 0:
                    break
                else:
                    incompletebrackets -= 1
        bracket2loc += 1
        siblingnumber += 1
    return bracket2loc

def make2childopnode(element, siblings, name):
    #for nodes such as power, fractions etc which always have 2 children
    # print("making: " + name)
    return Operator(name, check_pnode(element[0], []), check_pnode(element[1], []), element.attrib)

def make1childopnode(element, siblings, name):
    # print("making: " + name)
    #sqrt
    # do they not have siblings always?
    return Operator(name, check_pnode(element[0], child_list(element)), None, element.attrib)

def opfirst(element, siblings, name):
    # op was first child
    if len(siblings) == 1:
        newsibs = []
    if len(siblings) > 1:
        newsibs = siblings[1:]
    # print("making 1op: " + name)
    # do they always not have siblings ?
    # print("type", Operator(name, check_pnode(siblings[0], newsibs), None, element.attrib).get_name())
    return Operator(name, check_pnode(siblings[0], newsibs), None, element.attrib)

def opsecond(element, siblings, name):
    # the operator was first sibling, make and remove
    # can only currently get here if the current element has at least 1 sibling
    #could condense this to reduce repeats but this makes the intentions easier to read
    if len(siblings)==1:
        child1 = None
    elif len(siblings) == 2:
        child1 = check_pnode(siblings[1], [])
    else:  # ie len sibs > :
        child1 = check_pnode(siblings[1], siblings[2:])
    # print("making 2op: " + name)
    return Operator(name, check_pnode(element, []), child1 , siblings[0].attrib)

def opthird(element, siblings, name):
    # print("making 3op: " + name)
    return Operator(name, check_pnode(element, siblings[:1]), check_for_psiblings(siblings[2:]), siblings[1].attrib)
    # return Operator(name, make_pnode("mi", siblings[0], [], siblings[0].text), check_for_psiblings(siblings[2:]),
    #                 siblings[1].attrib)

def leafnode(type, element, siblings, name):
       if type == "mn":
        # make a value node
        sibling = check_for_psiblings(siblings)
        # print("making mn: " + name)
        return Value(name, sibling, element.attrib)  # keeps any attribs from mn
       if type == "mi":
           #make identifier node
           sibling = check_for_psiblings(siblings)
           # print("making mi: " + name)
           if element.attrib.get("mathvariant") == "double-struck":
               numbersetdict = {
                   "P": "primes",
                   "Q": "rationals",
                   "R": "reals",
                   "C": "complexes",  # &#x2102;"
                   "Z": "integers",
                   "N": "naturalnumbers"
                }
               return NumberSet(numbersetdict.get(name), element.attrib)
               #this is a number set such as reals, integers etc

           else:
               return Identifier(name, sibling, element.attrib)  # keeps any attribs from mi
       else:
           pass

#made this for help with more complex bracket scenarios
def make_bracket_node(type, element, siblings, bracket2loc ):
    #note, bracket1loc is element
    if type == "opafter":
        #the brackets
        #the operator after the brackets
        # print("making op after bracket: " + siblings[bracket2loc +1].text) #correct
        print("here op after" + name)
        return Operator(siblings[bracket2loc +1].text, check_pnode(element, siblings[:bracket2loc +1]), check_for_psiblings(siblings[bracket2loc +2:]), siblings[bracket2loc +1].attrib)

    if type == "justbrackets":
        # print("making justbrackets: " + element.text.strip() + siblings[bracket2loc].text.strip())
        return Brackets(element.text.strip(), siblings[bracket2loc].text.strip(), check_for_psiblings(siblings[:bracket2loc]), element.attrib)
    # if type == "emptybrackets":
    #     print("making empty brackets: " + element.text.strip() + siblings[bracket2loc].text.strip())
    #     return Brackets(element.text.strip(), siblings[bracket2loc].text.strip(),
    #                     check_for_psiblings(siblings[:bracket2loc]), element.attrib)
    if type == "mfenced":
        openbrac = element.attrib.get("open")
        closebrac = element.attrib.get("close")
        separators = element.attrib.get("separators")
        defaults = ["(", ")", ","]
        #if no values are found then allocate the defaults
        if openbrac == None:
            openbrac = defaults[0]
        if closebrac == None:
            closebrac = defaults[1]
        if separators == None:
            separators = defaults[2]
        # print("open, close, seps: ", openbrac, closebrac, separators)
        #mfenced can have 0 children
        try:
            return Brackets(openbrac , closebrac, handle_mfenced(element[0], child_list(element), separators), element.attrib)
        except IndexError:
            return Brackets(openbrac,closebrac, None , element.attrib)


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

def handle_mfenced(element,siblings, separators):
    #the children of 'mfenced' are whats passed to this method
    # print("HANDLING MFENCED")

    if siblings == []:
        return check_pnode(element,siblings)
    if len(siblings) == 1:
        return Operator(separators[0],check_pnode(element,[]), check_pnode(siblings[0],[]),{"separator":"true"})
    if len(siblings)>1:
        return mfenced_multichildren(element,siblings,separators)

def mfenced_multichildren(element,siblings , separators):
    if len(separators)>1:
        separators = separators[1:]
    else:
        pass
    return Operator(separators[0],check_pnode(element,[]), handle_mfenced(siblings[0], siblings[1:],separators),{"separator" :"true"})


'''END OF PRES ML'''

'''Parsing content ML into the internal tree structure'''

def check_cnode(element, siblings):
    ignore = ["math" ,"apply", "reln"]
    considerdict={
        "plus":"+",
        "minus":"-",
        "times":"&#8290;", #invisible times
        "divide": "/",
        "eq":"=",
        "neq":"&#x2260;",
        "approx": "&#x2243;",
        "equivalent":"&#8801;",
        "geq":"&#x2265;",
        "leq":"&#x2264;",
        "gt": "&#x3e;",
        "lt":"&#x3c;",
        "sin":"sin",
        "cos":"cos",
        "tan":"tan",
        "root": "sqrt",
        "power":"power",
        "factorial": "!",
        "not": "&#172;",
        "factorof":"&#xFF5C;",
        "in" : "&#x2208;",
        # "complexes": "complexes",#&#x2102;"
        # "integers":"integers",
        "emptyset":"emptyset",
        "eulergamma": "eulergamma",
        "ln": "ln",
        "exponentiale":"exponentiale",
        "and": "and",
        "false":"false",
        "imaginaryi": "imaginaryi",
        "infinity": "infinity",
        # "naturalnumbers": "naturalnumbers",
        "notanumber": "notanumber",
        "pi":"pi",
        # "primes":"primes",
        # "rationals": "rationals",
        # "reals":"reals",
        "or":"or",
        "true":"true",
        "abs":"abs",
        "rem":"rem",
        "gcd":"gcd",
        "lcm":"lcm",
        "xor":"xor",
        "implies":"implies",
        "arg":"arg",
        "floor": "floor",
        "list": "()",
        "set": "{}",
        "card":"card",#cardinality ||
        "cartesianproduct":"cartesianproduct",
        "vectorproduct": "vectorproduct",

    }
    numbersetdict = {
        "primes": "primes",
        "rationals": "rationals",
        "reals": "reals",
        "complexes": "complexes",  # &#x2102;"
        "integers": "integers",
        "naturalnumbers": "naturalnumbers"
    }
    leaf = ["cn", "ci"]
    tag = get_tag(element)

    # the element is the only xml node available for consideration
    if len(siblings) == 0:
        if tag in ignore:
            return check_cnode(element[0], child_list(element))
        if tag in leaf:
            if tag == leaf[0]: #cn
                return make_cnode("cn", element, siblings, element.text)
            if tag == leaf[1]:
                return make_cnode("ci", element, siblings, element.text)
        if tag == "interval":
            return make_interval_node(element,siblings)
        if tag == "list" or tag == "set":
            return make_cnode(tag , element, siblings, considerdict.get(tag) )
        if numbersetdict.get(tag) != None:
            return make_cnode("numberset", element, siblings, numbersetdict.get(tag))
        if considerdict.get(tag) != None:
            return make_cnode("operator", element, siblings, considerdict.get(tag))
    #the element and one sibling xml node are what is available for consideration
    if len(siblings) == 1:
        if tag in ignore:
            print("add some logic here")
        if numbersetdict.get(tag) != None:
            return make_cnode("numberset", element, siblings, numbersetdict.get(tag))
        if considerdict.get(tag) != None:
            return make_cnode("operator", element, siblings, considerdict.get(tag))
        if tag == "interval":
            return make_interval_node(element,siblings)
        if tag == "list" or tag == "set":
            return make_cnode(tag , element, siblings, considerdict.get(tag))

    if len(siblings) >1:
        if tag == "quotient":
            return make_cnode("quotient", element, siblings, "floor")
        elif considerdict.get(tag) != None:
            return make_cnode("operator", element, siblings, considerdict.get(tag))
        elif tag == "interval":
            return make_interval_node(element,siblings)
        elif tag == "list" or tag == "set":
            return make_cnode(tag , element, siblings, considerdict.get(tag))
        else:
            print("len(siblings) >1 logic needs adding")

    else:
        print("logic missing, help!")




def make_cnode(type, element, siblings, name):
    #Value nodes
    if type == "cn":
        # print("making cn: " + name)
        return Value(name, None, element.attrib)
    #Identifier nodes
    if type == "ci":
        # print("making ci: " + name)
        return Identifier(name, None, element.attrib)
    if type == "operator":
        # print("making op: " + name)
        return Operator(name, get_op_child(element,siblings), check_op_siblingsc(element, siblings), element.attrib  )
    if type == "quotient":
        # print("making quotient: " + name)
        firstchild = make_cnode("operator", element, siblings, "/")
        secondchild = None
        return Operator(name, firstchild, secondchild, element.attrib )

    if type == "list" or type =="set":
        operatorchildren = get_children(element)
        if len(operatorchildren) == 0:
            #empty list
            child0 = None
        if len(operatorchildren) == 1:
            #length 1 list
            child0 = check_cnode(operatorchildren[0],[])
        if len(operatorchildren) == 2:
            child0 = Operator(",", check_cnode(operatorchildren[0],[]),
                              check_cnode(operatorchildren[1],[]), {"separator": "true"})
        if len(operatorchildren) >2:
            child0 = Operator(",", check_cnode(operatorchildren[0],[]),
                              make_cnode("separator", operatorchildren[1],operatorchildren[2:], ","), {"separator": "true"})
        attributesdict = element.attrib
        attributesdict[type]= "true"
        return Brackets(name[0], name[1], child0 , attributesdict )

    if type == "separator":
        if len(siblings)<2:
            #i.e. one element, make this the 'other' child of the separator
            child1 = check_cnode(siblings[0],[])
        else:
            # 2 or more children requires another separator node, make this the 'other' child
            child1 = make_cnode("separator", siblings[0],siblings[1:], ",")
        return Operator(",", check_cnode(element,[]), child1, {"separator": "true"})

    if type== "numberset":
        return NumberSet(name, {"mathvariant":"double-struck"})





def make_interval_node(element, siblings):
    intervaltype = element.attrib.get("closure")

    # because the default value is closed []
    openbrac = "["
    closebrac = "]"
    separator = ","

    if intervaltype == "open":
        openbrac = "("
        closebrac = ")"
    if intervaltype == "open-closed":
        openbrac = "("
    if intervaltype == "closed-open":
        closebrac = ")"
    separatornode = Operator(separator, check_cnode(element[0], []), check_cnode(element[1],[]), {"separator": "true"})
    # print("Making interval node")
    return Interval(openbrac, closebrac, separatornode,element.attrib)


'''helper method for checking what the sibling for an operator node is'''
def check_op_siblingsc(element, siblings):
    # returns value for siblings
    if len(siblings) <= 1:
        opsibling = None
    if len(siblings) == 2:
        opsibling = check_cnode(siblings[1], [])
    if len(siblings) > 2:
        opsibling = check_cnode(element, siblings[1:])
    return opsibling

def get_op_child(element,siblings):
    #returns what the value for the operators first child is
    if siblings == []:
        opchild = None
    else:
        opchild = check_cnode(siblings[0], [])
    return opchild

def get_children(element):
    #returns list of elements children
    list = []
    for child in element:
        list.append(child)
    return list