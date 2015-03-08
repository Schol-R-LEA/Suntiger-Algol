#/usr/bin/python3

# part of the Suntiger Algol project
# initiated 2008:05:23, by Joseph Osako, Jr. <josephosako@gmail.com>
# file last modified 2015:03:08


from CompilerExceptions import DuplicateSymbolException
from Symbol import Symbol, Identifier
from typecheck import typecheck



class SymbolTable(dict):
    """Base class for symbol tables
    
    @instance parent: SymbolTable
    @instance children: list of SymbolTable
    @instance descr: string
    
    A SymbolTable is a dictionary which holds Symbol objects.
    The individual tables serve as nodes to an implicit tree structure
    holding all of the tables for the scopes, both current and expired.
    Each table has a parent reference (which may be empty in the case of
    the top-level table) and a list of zero or more child tables. Finally,
    each table has a (non-unique) text description which is used as
    a simple check against mismatches.
    """
    @typecheck
    def __init__(self, parent = None, descr: str = "Top"):
        """Constructor

        Initializes the instance variables _symbols, _parent,
        and _children. If __parent is not null, it adds the new
        SymbolTable to the parent table's list of children.
        """
        self.__parent = parent
        self.__children = list()
        self.__descr = descr
        self.__symbols = 0
        if parent is not None:
            parent.__children.append(self)


    #@takes("SymbolTable", Symbol)
    @typecheck
    def insert(self, sym: Symbol):
        """Add a symbol to the table.
        
        @params sym: a Symbol object
        
        The function gets the name of the symbol to use as it's
        table key. Then, if there is no key of that name in the
        table, it inserts the key:symbol pair (note that it only checks
        the current scope, not it's parent). If a key with that
        name already exists, an exception is raised to notify the
        error handler that the compiler tried to insert a duplicate
        key (the compiler should never try to do this).
        """
        key = sym.getName()
        
        if key not in self:
            self[key] = sym
            self.__symbols += 1
        else:
            raise DuplicateSymbolException(key, self.__descr)
        

    @typecheck
    def find(self, key: str):
        """Find a symbol in the table.
        
        @returns A symbol if successful, None if not.
        
        find() first checks the local dictionary to see if there
        is a symbol by the given name in it, and returns it if
        there is.
        """
        key = key
        if key in self:
            return self[key]
        
    def find_in_scope(self, key):
        """Find a symbol in the table or any of it's parents.
        
        @returns A symbol if successful, None if not.
        
        find() first checks the local dictionary to see if there
        is a symbol by the given name in it, and returns it if
        there is. If there isn't, and the table has a parent
        table, it recurses up the chain; otherwise, it returns None.
        """
        found = self.find(key)
        if found:                           # found in the current table
            return found
        elif self.__parent is not None:     # check the rest of the curr. scope
            return self.__parent.find_in_scope(key)
        else:
            return False

    def depth(self):
        """Returns the nesting depth of the table."""
        if self.__parent is None:
            return 0
        else:
            return 1 + self.__parent.level()


    def size(self):
        """ Returns the number of symbols in the table,
        and the number of children the table has. This
        only gets the table's own symbols and children,
        not the whole sum for it's descendants.
        """
        return self.__symbols, len(self.__children)
    
    def children(self):
        """Get the list of child tables for this table."""
        return self.__children

    def __repr__(self):
        """ Create a string representation of the table
        
        @returns string: the display form of the table
        The method has three parts: the first
        """
        # print the current block descriptor on a separate line,
        s = '\n' + self.getScope() + ':\n'
        # print all of the symbols in the top of the current branch scope.
        if len (self) != 0:
            for sym in self:
                s += sym + ' - ' + repr(self[sym]) + '\n'
                
        # print each of child blocks of the table.
        if len(self.__children) > 0:
            # recurse down into each subtable
            for child in self.__children:
                s += repr(child)
        return s
    
    ## Accessors
    
    def getParent(self):
        """Accessor for the table parent property"""
        return self.__parent
    
    def getDescr(self):
        """Accessor for the scope description"""
        return self.__descr

    def getScope(self):
        """Returns a string representing the current nested scope.
        
        The returned string has the block descriptors of the each of
        the successive blocks from the global scope to the current one,
        with the descriptions separated by forward slashes.
        """
        s = self.__descr
        if self.__parent is None:
            return s
        else:
            return self.__parent.getScope() +  '.' + s


#############################################
# test section
"""The test code for SymbolTable creates a top-level
SymbolTable and several child tables which are added to it.
It then creates an exception frame and tests adding

"""
if __name__ == "__main__":
    print("SymbolTable class self-test")
    print("*******************")
    
    top = SymbolTable()
    some_blk = SymbolTable(top, 'some')
    for_blk = SymbolTable(top, 'for')
    while_blk = SymbolTable(for_blk, 'while')
    while_blk2 = SymbolTable(top, 'while')
    
    try:
        print("foo", end=' ')
        if top.find('foo'):
            print("exists", end=' ')
        else:
            print("does not exist", end=' ')
        print("in", top.getScope())
        top.insert(Identifier('foo'))

        print("foo", end=' ')
        if top.find('foo'):
            print("exists", end=' ')
        else:
            print("does not exist", end=' ')
        print("in ", top.getScope())

        top.insert(Identifier('bar'))
        some_blk.insert(Identifier('baz'))
        # test local scope
        print("baz", end=' ')
        if some_blk.find('baz'):
            print("exists", end=' ')
        else:
            print("does not exist", end=' ')
        print("in ", some_blk.getScope())
        
       # for_blk.insert(Identifier('foo'))
        for_blk.insert(Identifier('quux'))
        while_blk.insert(Identifier('blech'))
        # at top level
        print("foo", end=' ')
        if while_blk.find_in_scope('foo'):
            print("exists", end=' ')
        else:
            print("does not exist", end=' ')
        print("in ", while_blk.getScope())

        # at intermediate level
        print("quux", end=' ')
        if while_blk.find('quux'):
            print("exists", end=' ')
        else:
            print("does not exist", end=' ')
        print("in", while_blk.getScope())

        # at local level
        print("blech", end=' ')
        if while_blk.find('blech'):
            print("exists", end=' ')
        else:
            print("does not exist", end=' ')
        print("in", while_blk.getScope())

         # in a different scope - should not find it
        print("baz", end=' ')
        if while_blk.find('baz'):
            print("exists", end=' ')
        else:
            print("does not exist", end=' ')
        print("in", while_blk.getScope())
    
        while_blk.insert(Identifier('zark'))
        top.insert(Identifier('grue'))
        while_blk2.insert(Identifier('quux'))
        top.insert(Identifier('flarp'))
        
        print(top)
        
    except DuplicateSymbolException as e:
        print("DuplicateSymbolException: " + repr(e))

