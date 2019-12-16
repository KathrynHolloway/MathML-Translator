
# """Usage:
# app.py translate (cont2pres | pres2cont) <filein> <fileout>
# app.py -h | --help
# """
# from docopt import docopt
# if __name__ == '__main__':
#     arguments = docopt(__doc__, version='0.1.1rc')
#     print(arguments)

"""Usage:
app.py translate (cont2cont | pres2pres | cont2pres | pres2cont) <filein> <fileout>
app.py parse (cont|pres) <filein> <fileout>
app.py -h | --help


"""
from docopt import docopt
from parsing import *
from nodes import Node
from xmlout import contxmlout, presxmlout
import os

def translate(arguments):
    # file_location = "interval3cont.xml"#input("Please enter the location of your file: ")
    input_file_loc = arguments.get("<filein>")
    output_file_loc = arguments.get("<fileout>")

    '''no translation'''
    cont2cont = arguments.get("cont2cont")
    pres2pres = arguments.get("pres2pres")

    '''translation'''
    cont2pres = arguments.get("cont2pres")
    pres2cont = arguments.get("pres2cont")

    # parse the input file
    parsed_doc = doc_parse(input_file_loc)
    '''MAKES IT TO HERE'''
    if cont2cont == True:
        # use the parsed content ml file and convert it to internal tree structure
        tree = make_contentml_tree(parsed_doc)
        # output to the given file location, the requested pres xml
        contxmlout(tree, output_file_loc)

    elif pres2pres == True :
        # use the parsed content ml file and convert it to internal tree structure
        tree = make_presml_tree(parsed_doc)
        # output to the given file location, the requested pres xml
        presxmlout(tree, output_file_loc)

    elif cont2pres == True:
        # use the parsed content ml file and convert it to internal tree structure
        tree = make_contentml_tree(parsed_doc)
        # output to the given file location, the requested pres xml
        presxmlout(tree, output_file_loc)

    elif pres2cont == True:
        # use the parsed presentation ml file and convert it to internal tree structure
        tree = make_presml_tree(parsed_doc)
        # output to the given file location, the requested content xml
        contxmlout(tree, output_file_loc)

    else:
        print("I didn't do anything useful, sorry")

def parse(arguments):
    # file locations
    input_file_loc = arguments.get("<filein>")
    output_file_loc = arguments.get("<fileout>")
    # parse the input file
    parsed_doc = doc_parse(input_file_loc)

    if arguments.get("cont")== True:
        tree = make_contentml_tree(parsed_doc)
        contxmlout(tree,output_file_loc )

    if arguments.get("pres")== True:
        tree = make_presml_tree(parsed_doc)
        presxmlout(tree,output_file_loc )


if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1.1rc2')
    print(arguments)
    if arguments.get("translate") == True:
        translate(arguments)
    if arguments.get("parse")== True:
        parse(arguments)



# docparse(input_file_loc)
#
# tree = Node("apply",
#             Node("plus",
#                  Node("cn",Node("3",None, None),
#                       Node("cn",Node("4",None, None),None)),None), None)

# print(tree.tag , tree.child.child.child.tag , tree.sibling)
# tree.sibling = "This"
# print( tree.sibling)

'''make the internal tree representation'''
'''ADD THIS LOGIC TO CATCH ERRORS ABOVE?######################################################################'''
# try:
#     tree = make_tree(input_file_loc)
# except OSError:
#     print("Couldn't find that file, please try again.")


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

''''Testing mfenced1pres.xml''' '''pass'''
# print(tree.get_openbrac()) #(
# print(tree.get_closebrac()) #)
# print(tree.get_child().get_name()) #,
# print(tree.get_child().get_child().get_name()) #x
# print(tree.get_child().get_nextchild().get_name()) #y

'''Testing interval1cont.xml''' '''pass'''
# print(tree.get_openbrac()) #[
# print(tree.get_closebrac()) #]
# print(tree.get_child().get_name()) #,
# print(tree.get_child().get_child().get_name()) #x
# print(tree.get_child().get_nextchild().get_name()) #x

# print(os.getcwd())
# print(tree.child.child.sibling.sibling.child.sibling.sibling.attributes.items() )
# '''dictionary of attributes'''
#
# '''print out the presentation xml tree'''
# print(presxmlout(tree))

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


