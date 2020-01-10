"""Usage:
app.py translate (cont2cont | pres2pres | cont2pres | pres2cont) <filein> <fileout>
app.py parse (cont|pres) <filein> <fileout>
app.py -h | --help


"""
from docopt import docopt
from parsing import doc_parse, make_contentml_tree, make_presml_tree
from nodes import Node
from xmlout import contxmlout, presxmlout
import os

def translate(arguments):
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



