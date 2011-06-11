#!/usr/bin/python
"""Simple filter program that takes an stream of braces and identifiers
and builds a symbol table from it. When the stream exists, it returns the
symbol table."""

from MasterSymbolTable import MasterSymbolTable
from Symbol import Identifier
from CompilerExceptions import *
import sys

symtab = MasterSymbolTable()
scope_lvl = 0
scope_cnt = 0

for line in sys.stdin:
    line.strip()      # remove trailing whitespace
    if len(line) < 1: # if the line is empty, go to the next one
        continue
    
    else:
        # break the line into tokens by whitespace
        tokens = line.split()
        
        #
        while len(tokens) > 0:
            token = tokens.pop()
            token.strip()

            # this is the main set of comparisons. If it finds an open
            # brace, it creates a new scope. If it finds a close brace, 
            # it tries to exit the current scope, throwing an exception
            # if it is at the top already. Otherwise, checks if the
            # symbol is in the current table (*not* the current scope, just
            # the one table) and if it isn't, inserts it.
            if token == '{':
                scope_lvl += 1
                scope_cnt += 1
                symtab.enter('Scope' + str(scope_cnt))
            elif token == '}':
                scope_lvl -= 1
                try:
                    if scope_lvl == 0:
                        symtab.exit('Top') 
                    else:
                        symtab.exit('Scope' + str(scope_cnt))
                except NestingException, e:
                     sys.stderr.write(str(e))      # print an error and press on
            else:
                if symtab.find(token) is None:
                    try:
                        symtab.insert(Identifier(token))
                    except DuplicateSymbolException, e:
                        sys.stderr.write(str(e))   # print an error and press on

if scope_lvl > 0:
    sys.stderr.write(str(scope_lvl) + " unclosed blocks\n")
    
# all symbols processed, print table
print symtab
