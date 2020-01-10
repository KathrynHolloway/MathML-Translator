from lxml import etree

def optimise(tree):
    '''the following two nodes are always present and necessary'''
    newoptimisedtree = etree.Element(tree.tag, xmlns="http://www.w3.org/1998/Math/MathML") # math
    mrow = etree.SubElement(newoptimisedtree, "mrow")
    '''note: cannot just trace the tree and remove unnecessary nodes as this looses any descendants also'''

    #check the child(ren) of the first mrow before iterating through the rest of the tree
    check_element(tree[0], mrow)

    return newoptimisedtree

def check_element(current, newnodesparent): #checks whether the next element should be made
    #note that current is the location on the original tree and newnodesparent referrs to a node in the new tree
    children = get_list_of_children(current)
    if current.tag == "mrow" and len(children) == 1 and children[0].tag == "mrow":
        # the current element is mrow with only child also an mrow element, don't make the child
        #move on to checking the children of the child
        check_element(current[0], newnodesparent)
    else:
        #make then check each of the child(ren)
        for child in children:
            newelement = etree.SubElement(newnodesparent, child.tag, child.attrib)
            newelement.text = child.text
            check_element(child, newelement )


def get_list_of_children(element):
    children = []
    for child in element:
        children.append(child)

    return children

