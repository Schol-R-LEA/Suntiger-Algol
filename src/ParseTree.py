# part of the Suntiger Algol project
# initiated 2008:05:23, by Alice Osako <alicetrillianosako@gmail.com>
# file last modified 2022:02:11

from Symbol import Symbol
from SymbolTable import SymbolTable

class ParseTree(object):
    subtrees = list()
    
    def __init__(self):
        pass
    
    pass

class ParseTreeNode(object):
    def __init__(self, node_symbol, left_leaf, right_leaf):
        self.__node_symbol = node_symbol
        self.__left_leaf = left_leaf
        self.__right_leaf = right_leaf
    
            
