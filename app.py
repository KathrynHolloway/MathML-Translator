from parsing import *
from nodes import Node
from xmlout import xmlout
import os
file_location = 'brackets1.xml'#"pres_token_elements_1.xml"#input("Please enter the location of your file: ")

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
tree = make_tree(file_location)

# print(tree.name) #=
# print(tree.child.name) # x
# print(tree.child.sibling.name) #2
# print(tree.attributes)

'''testing x=2pres.xml'''
# print(tree.get_name()) #=
# print(tree.get_child().get_name()) # x
# print(tree.get_nextchild().get_name()) #2

'''testing quadformpres4.xml'''
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

'''testing brackets1.xml'''
print(tree) #-
# print(tree.get_child().get_name()) # ()
# print(tree.get_nextchild().get_name()) #7
# print( tree.get_child().get_child().get_name()) #+
# print( tree.get_child().get_child().get_child().get_name()) # x
# print( tree.get_child().get_child().get_nextchild().get_name()) # 2


# print(os.getcwd())
# print(tree.child.child.sibling.sibling.child.sibling.sibling.attributes.items() )
# '''dictionary of attributes'''
#
'''print out the xml tree'''
# print(xmlout(tree))
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


