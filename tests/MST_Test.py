#!/usr/bin/python3

from Symbol import *
from SymbolTable import *
from MasterSymbolTable import *

"""The self-test for MasterSymbolTable consists of:
    * creating a MST
    * testing that a find on the empty table fails
    * insert symbols into the top level table and test if it can be found
    * create nested scopes and inserting symbols into them,
      testing if a) they are found, and b) if the are no longer
      found when the scope exits
    * test whether symbols in the parent scope are found within the child scope
    * print the whole symbol table
    * test the error checking
"""
print("MasterSymbolTable class self-test")
print("*******************")

from Symbol import Identifier
symtab = MasterSymbolTable()
try:
    print("Performing a search on an empty table:")
    print("foo", end=' ')
    if symtab.find('foo'):
        print("exists", end=' ')
    else:
        print("does not exist", end=' ')
    print("in", symtab.getScope())

    print()
    print("Populating table:")
    symtab.insert(Identifier('foo'))

    print("Adding 'foo' to", symtab.getScope())
    print("foo", end=' ')
    if symtab.find('foo'):
        print("exists", end=' ')
    else:
        print("does not exist", end=' ')
    print("in ", symtab.getScope())

    print("Adding 'bar' to", symtab.getScope())
    symtab.insert(Identifier('bar'))

    symtab.enter('flooby')
    print("Entering new scope:", symtab.getScope())
    
    print("Nested scope test: Adding 'foo' to", symtab.getScope())
    symtab.insert(Identifier('foo'))
    print("foo", end=' ')
    if symtab.find('foo'):
        print("exists", end=' ')
    else:
        print("does not exist", end=' ')
    print("in ", symtab.getScope())
    
    symtab.insert(Identifier('quux'))
    print("quux", end=' ')
    if symtab.find('quux'):
        print("exists", end=' ')
    else:
        print("does not exist", end=' ')
    print("in ", symtab.getScope())
    symtab.exit('flooby')
    symtab.insert(Identifier('flarp'))
    symtab.enter('for')
    symtab.insert(Identifier('blech'))
    symtab.insert(Identifier('zark'))
    symtab.enter('while')
    print("quux", end=' ')
    if symtab.find('quux'):
        print("exists", end=' ')
    else:
        print("does not exist", end=' ')
    print("in ", symtab.getScope())
    symtab.insert(Identifier('grue'))
    symtab.insert(Identifier('quux'))
    symtab.exit('while')
    symtab.exit('for')
    
    print()
    print("Symbol Table:")
    print(symtab)

except DuplicateSymbolException as e:
    print("DuplicateSymbolException: " + repr(e))
except NestingException as e:
    print("NestingException: " + repr(e))
except BottomOfTableStackException as e:
    print("BottomOfTableStackException: " + repr(e))

print()
print("Error checking tests")
try:
    print("Test detection of duplicate symbols:")
    symtab.insert(Identifier('foo'))
except DuplicateSymbolException as e:
    print("DuplicateSymbolException: " + repr(e))

print()
try:
    print("Test detection of nesting errors:")
    symtab.exit('nonexistent')
except NestingException as e:
    print("NestingException: " + repr(e))

print()
try:
    print("Test detection of the bottom of the stack:")
    symtab.exit('Top')
except BottomOfTableStackException as e:
    print("BottomOfTableStackException: " + repr(e))		
