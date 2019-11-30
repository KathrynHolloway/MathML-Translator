from parsing import *
from nodes import Node
from xmlout import *
import os
file_location = "(a)pres.xml"#input("Please enter the location of your file: ")

# docparse(file_location)
# 
# tree = Node("apply",
#             Node("plus",
#                  Node("cn",Node("3",None, None),
#                       Node("cn",Node("4",None, None),None)),None), None)

# print(tree.tag , tree.child.child.child.tag , tree.sibling)
# tree.sibling = "This"
# print( tree.sibling)

'''make the internal tree representation'''
try:
    tree = make_tree(file_location)
except OSError:
    print("Couldn't find that file, please try again.")


'''testing x=2pres.xml''' '''pass'''
# print(tree.get_name()) #=
# print(tree.get_child().get_name()) # x
# print(tree.get_nextchild().get_name()) #2

'''testing quadformpres4.xml''' '''pass'''
# print(tree.get_name()) #=
# print(tree.get_child().get_name()) # x
# print(tree.get_nextchild().get_name()) #/
# print( tree.get_nextchild().get_child().get_name()) #+-
# print( tree.get_nextchild().get_nextchild().get_name()) # *
#
# print( tree.get_nextchild().get_child().get_child().get_name()) #-
# print( tree.get_nextchild().get_child().get_child().get_child().get_name()) #b
#
# print( tree.get_nextchild().get_child().get_nextchild().get_name()) # sqrt
# print( type(tree.get_nextchild().get_child().get_nextchild().get_name())) # str
# print( type(tree)) # operator

'''testing brackets1.xml''' '''PASSS'''
# print(tree.get_name()) # not none type
# print(tree.get_child().get_openbrac()) # (
# print(tree.get_child().get_closebrac()) #)
# print(tree.get_nextchild().get_name()) #7
# print( tree.get_child().get_child().get_name()) #+
# print( tree.get_child().get_child().get_child().get_name()) # x
# print( tree.get_child().get_child().get_nextchild().get_name()) # 2

'''testing (a)pres.xml''' '''PASS'''
# print(tree.get_openbrac()) # (
# print(tree.get_closebrac()) # )
# print(tree.get_child().get_name()) #a

'''Testing addcont.xml''' '''pass'''
# print(tree.get_name()) # +
# print(tree.get_child().get_name()) # x
# print(tree.get_nextchild().get_name()) #+
# print( tree.get_nextchild().get_child().get_name()) #y
# print( tree.get_nextchild().get_nextchild().get_name()) #z

'''Testing sinxcont.xml ''' '''pass'''
# print(tree.get_name()) #sin
# print( tree.get_child().get_name()) #x

'''Testing quadformcont.xml''' '''Pass'''
# print(tree.get_name()) #=
# print(tree.get_child().get_name()) # x
# print(tree.get_nextchild().get_name()) #/
# print( tree.get_nextchild().get_child().get_name()) #+-
# print( tree.get_nextchild().get_nextchild().get_name()) # *
#
# print( tree.get_nextchild().get_child().get_child().get_name()) #-
# print( tree.get_nextchild().get_child().get_child().get_child().get_name()) #b
#
# print( tree.get_nextchild().get_child().get_nextchild().get_name()) # sqrt
# print( tree.get_nextchild().get_child().get_nextchild().get_child().get_name()) # -
# print( tree.get_nextchild().get_child().get_nextchild().get_child().get_child().get_name()) # power
#
# print( tree.get_nextchild().get_child().get_nextchild().get_child().get_child().get_child().get_name()) # b
# print( tree.get_nextchild().get_child().get_nextchild().get_child().get_child().get_nextchild().get_name()) # 2
#
# print( tree.get_nextchild().get_child().get_nextchild().get_child().get_nextchild().get_name()) # *
# print( tree.get_nextchild().get_child().get_nextchild().get_child().get_nextchild().get_child().get_name()) # 4
# print( tree.get_nextchild().get_child().get_nextchild().get_child().get_nextchild().get_nextchild().get_name()) # *
# print( tree.get_nextchild().get_child().get_nextchild().get_child().get_nextchild().get_nextchild().get_child().get_name()) # a
# print( tree.get_nextchild().get_child().get_nextchild().get_child().get_nextchild().get_nextchild().get_nextchild().get_name()) # c
#

'''Testing factorialcont.xml and factorialpres.xml'''
# print(tree.get_name()) #!
# print(tree.get_child().get_name()) #3 or 7

'''Testing sinpres.xml''' '''PASS'''
# print("TOP LEVEL NODE TYPE = " , tree) #None
# print(tree.get_name()) #sin
# print(tree.get_child().get_name()) # x\


# print(os.getcwd())
# print(tree.child.child.sibling.sibling.child.sibling.sibling.attributes.items() )
# '''dictionary of attributes'''
#
# '''print out the presentation xml tree'''
print(presxmlout(tree))

'''print out the content xml tree'''
# print(contxmlout(tree))
#
# print(tree.child.child.name) # mi
#
# print(tree.child.child.sibling.child.name) # =
#
# print(tree.child.child.sibling.name) #mo
# print(tree.child.child.sibling.sibling.name) #mfrac
#
# #some deeper nodes
# print( tree.child.child.sibling.sibling.child.child.sibling.sibling.child.child.sibling.sibling.child.child.name) #4
# print( tree.child.child.sibling.sibling.child.child.sibling.sibling.child.child.sibling.sibling.child.sibling.sibling.sibling.sibling.child.name) #c


