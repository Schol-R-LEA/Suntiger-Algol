#!/usr/bin/python3

# part of the Suntiger Algol project
# initiated 2008:04:06, by Joseph Osako, Jr. <JoeJr@osakoweb.com>
# file last modified 2010:01:11

from Symbol import Symbol
from SymbolTable import SymbolTable
from CompilerExceptions import *
from typecheck import typecheck



class MasterSymbolTable(object):
    """ Controller for a set of SymbolTables
    
    @instance head: root of the whole symbol table
    @instance current: current node, set to head initially
    
    The MasterSymbolTable manages scope through a branch in the
    Symbol Table tree. The MST holds two items: the root of the
    overall ST tree, and the current node in the tree.
    
    The majority of the methods of MST simply alias a call to the
    corresponding methods for the current table.
    """

    def __init__(self):
        """ Constructor
        
        Creates the root table and sets it to the current table.
        """
        self.__head = SymbolTable()
        self.__current = self.__head

    def enter(self, descr):
        """Enter a new scope
        
        @params descr: A description of the block being entered.
        @returns None
        Creates a new SymbolTable as a child of the current table,
        then sets the current table to the child table.
        """
        child = SymbolTable(self.__current, descr)
        self.__current = child
        
    def exit(self, descr):
        """Exit from the current scope to it's parent.
        
        Moves up to the current table node's parent node.
        Raises an exception if there is no parent for the
        current table.
        
        The value descr is used as consistency check - if the
        description at the exit does not match the one on enter,
        then there has been a nesting error and an exception is raised.
        """
        currdescr = self.__current.getDescr()
        if currdescr != descr:
            raise NestingException(currdescr, descr)
        elif self.__current.getParent() is None:
            raise BottomOfTableStackException(currdescr)
        else:
            self.__current = self.__current.getParent()

    def insert(self, sym):
        """ Insert a symbol into the current table."""
        return self.__current.insert(sym)

    def find(self, key):
        """ Find a symbol in the current table."""
        return self.__current.find(key)

    def find_in_scope(self, key):
        """ Find a symbol in the current table or any of it's parent tables."""
        return self.__current.find_in_scope(key)

    def __repr__(self):
        """Returns a string representation of the symbol table tree."""
        s = repr(self.__head)
        syms, blocks = self.size()
        # print the sums for symbols and sub-tables
        s += '\n' + str(syms) + ' symbols in ' + str(blocks) + " blocks\n"
        return s

    def getScope(self):
        """Returns the scope of the current table. """
        return self.__current.getScope()
    
    def size(self, symtab = None):
        """ Get the number of symbols and the number of blocks in the table.
        
        This sums the number of symbols in the current table
        and the number of symbols in it's children. It also sums the
        number of descendants. If it is the head of the table,
        it adds one in order to count itself.
        """
        if symtab is None:
            symtab = self.__head
        syms, children = symtab.size()
        for child in symtab.children():
            s, c = self.size(child)
            syms += s
            children += c
        if symtab == self.__head:
            children += 1
        return syms, children

########################################
# test section
if __name__ == "__main__":
    print("MasterSymbolTable class self-test")
    print("*******************")
    from Symbol import Identifier
    symtab = MasterSymbolTable()
    try:
        print("foo", end=' ')
        if symtab.find('foo'):
            print("exists", end=' ')
        else:
            print("does not exist", end=' ')
        print("in ", symtab.getScope())
        
        symtab.insert(Identifier('foo'))
        
        print("foo", end=' ')
        if symtab.find('foo'):
            print("exists", end=' ')
        else:
            print("does not exist", end=' ')
        print("in ", symtab.getScope())
        
        symtab.insert(Identifier('bar'))
        symtab.enter('flooby')
        print("foo", end=' ')
        if symtab.find('foo'):
            print("exists", end=' ')
        else:
            print("does not exist", end=' ')
        print("in ", symtab.getScope())
        print("foo", end=' ')
        if symtab.find_in_scope('foo'):
            print("exists", end=' ')
        else:
            print("does not exist", end=' ')
        print("in the scope of", symtab.getScope())
        symtab.enter('snarky')
        print("foo", end=' ')
        if symtab.find_in_scope('foo'):
            print("exists", end=' ')
        else:
            print("does not exist", end=' ')
        print("in the scope of", symtab.getScope())
        symtab.exit('snarky')
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
        #symtab.exit('Top')
            
        print(symtab.size())
        
        print(symtab)
    except DuplicateSymbolException as e:
        print("DuplicateSymbolException: " + repr(e))
    except NestingException as e:
        print("NestingException: " + repr(e))
    except BottomOfTableStackException as e:
        print("BottomOfTableStackException: " + repr(e))

        print("NestingException: " + repr(e))
