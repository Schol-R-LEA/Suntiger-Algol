#!/usr/bin/python3

# part of the Suntiger Algol project
# initiated 2008:04:06, by Joseph Osako, Jr. <JoeJr@osakoweb.com>
# file last modified 2010:01:11

from CompilerExceptions import KeywordException
from typecheck import typecheck


class Symbol(object):
    """Parent class for the symbol table entries.
    
    NOTE: This is intended as an abstract class, and shouldn't be
    instantiated. However, because Python does not support abstract
    classes (or interfaces), this is done on the honor system.
    """
    @typecheck
    def __init__(self):
        """Contructor
        
        Creates the instance variable name and initializes it to none.
        """
        self.__name = None
 
    @typecheck
    def __repr__(self) -> str:
        """Creates a string representation of the Symbol
        
        # @returns string
        
        Format:
            Type: <symbol type>
        """
        return "type: " + type(self).__name__


class Identifier (Symbol):
    """Symbol table entry class for identifiers.
    """
    @typecheck
    def __init__(self, name: str):
        """Constructor
        
        @params name: The name of the identifier. This should match the
        corresponding key in the symbol table.
        @type name: string
        """
        self.__name = name

        
    @typecheck
    def getName(self) -> str:
        """Accessor for the symbol name"""
        return self.__name

        
    @typecheck
    def __repr__(self) -> str:
        """Printable representation of an Identifier.

        # @returns string
        The format for identifiers is as follows:
            Type: Identifier, name: <name>
        This string is returned with no trailing newline.
        Note that this is also used for str() by default.
        """
        s = super(Identifier, self).__repr__() + ', '
        s += "name: " + self.__name
        return s
 

class Constant(Identifier):
    @typecheck
    def __init__(self, name: str, value: str, offset: int):
        """Constructor
        
        @params name: The name of the identifier. This should match the
        corresponding key in the symbol table.
        @type name: string
        """
        super(Constant, self).__init__(name)
        self.__value = value
        self.__location = offset

        @typecheck        
        def type(self) ->str:
            return "INT"
        

        def location(self):
            return self.__location



class Variable(Identifier):
    def __init__(self, name, type, offset):
        """Constructor
        
        @params name: The name of the identifier. This should match the
        corresponding key in the symbol table.
        @type name: string
        """
        super(Variable, self).__init__(name)
        self.__type = type
        self.__location = offset
        
    def __repr__(self) ->str:
        s = super(Variable, self).__repr__()
        s += ', vartype: ' + str(self.__type)
        s += ', location: ' + str(self.__location)
        return s
    
    def type(self):
        return str(self.__type)
    
    def location(self):
        return self.__location
    

class SystemRoutine(Identifier):

    @typecheck
    def __init__(self, name: str, code, argtype):
        super(SystemRoutine, self).__init__(name)
        self.__code = code
        self.__type = argtype


    def code(self, argtype):
        if argtype in self.__type or self.__type is None:
            return self.__code
        else:
            return False
        

#########################################
# test section
if __name__ == "__main__":
    print("Symbol class self-test")
    print("*******************")
    import doctest
    doctest.testmod()

    sym = Identifier('foo')
    sym2 = Identifier('bar')
    print(sym)
    print(sym2)
