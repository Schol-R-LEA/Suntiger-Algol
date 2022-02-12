#!/usr/bin/python3

# part of the Suntiger Algol project
# initiated 2008:05:23, by Alice Osako <alicetrillianosako@gmail.com>
# file last modified 2022:02:11

from sys import argv, exit
from io import StringIO

from tokens import Token
from st_parse import parse
from codegen import codegen
from CharBuffer import CharBuffer
from messages import error_handlers, lister
from MasterSymbolTable import MasterSymbolTable


# development information about the program
__authors__ = 'Alice Osako <alicetrillianosako@gmail.com>'
__version__ = '0.0.3'
__date__ = '2008:05:23'
__modified__ = '2022:02:11'

__copyright__ = """Suntiger Algol """ + __version__ + """ Copyright (c) 2008, 2022 the Suntiger Group (""" + __authors__ + """, et al.)
All rights reserved."""
__license__ = """Licensed under the OSI-BSD Open License.
See the file suntiger/docs/LICENSE for license details."""

__credits__ = """Uses Dimitri Dvoinikov's typecheck decorator library """
__credits__ += """<http://www.targeted.org/python/recipes/typecheck.py>\n"""
__credits__ += """for method typechecking.\n"""


__dedication__ = """To Dr. Edie Reiter of CSU East Bay, for whose """
__dedication__ += """Spring 2008 course on compiler design """
__dedication__ += """an implementation this was originally written."""


if __name__ == "__main__":
    global symtab
    if argv[1] == "--credits":
        print (__copyright__ + __license__ + '\n\n' + __credits__)
        exit(0)

    elif argv[1] == "--version":
        print(__version__ + '\n')
        exit(0)

    elif argv[1] == "--dedication":
        print(__dedication__ + '\n')
        exit(0)

    elif len(argv) != 2:
        print("usage: suntiger <filename>")
        exit(1)
    name = argv[1]
    
    try:
        src = open(name + '.al')
    except:
        print("Could not open source file")
        exit(-1)

    try:
        listing = open(name + '.lis', 'w')
    except:
        print("Could not create listing file")
        exit(-1)

    try:
        dest = open(name + '.s', 'w')
    except:
        print("Could not create  file")
        exit(-1)
    
    symtab = MasterSymbolTable()
    
    # this is a series of closures used to group functions
    # which have some global state. This is done to
    # avoid sharing globals between modules, at least as much
    # as possible.
    error, warning = error_handlers(symtab, listing, dest)
    print_listing = lister(listing) # get the listing function
    emit, emit_epilog, load, store = codegen(symtab, dest)
    get = Token.Tokenizer(CharBuffer(src), warning)
    
    parse(get, dest, print_listing, symtab, warning, error, emit, load, store)
    listing.write('\n\n' + str(symtab))
    emit_epilog()
    listing.close()
    dest.close()
    print()

