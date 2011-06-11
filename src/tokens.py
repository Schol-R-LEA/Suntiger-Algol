

# part of the Suntiger Algol project
# initiated 2008:05:23, by Joseph Osako, Jr. <JoeJr@osakoweb.com>
# file last modified 2010:01:11

from typecheck import typecheck
from CharBuffer import CharBuffer
from StateMachine import StateMachine, State
from string import ascii_letters, digits, whitespace


warning = None

class Token(object):
    """ Class for tokens, as well as the tokenizer.
    
    This class consists of four parts: a set of class constants
    representing different types of tokens, a static initializer for the
    lexical analyzer's state machine, the constructor and instance methods
    for the Token objects, and a class nethod that returns a generator
    object which tokenizes a CharBuffer source, returning the next token
    on each successive call.
    
    """
    # Token types for the lexical analyzer - this type of group return is used
    # as the Python equivalent of an Enum, setting each to a matching number in the
    # returned range.
    EOF, __WSPACE, \
    SEMI, BRACKET, PAREN, COMMA, \
    IDENT, CHARLIT, INTLIT, STRINGLIT, BOOLLIT, \
    MULOP, ADDOP, RELOP, NOTTOK, ASSIGN, \
    BASICTYPETOK, INTCONSTTOK, ARRAYTOK, PROCTOK, \
    BEGINTOK, ENDTOK, \
    IFTOK, THENTOK, ELSETOK, FITOK, \
    WHILETOK, DOTOK, ODTOK, \
    FORTOK, ROFTOK, UNTILTOK, STEPTOK, \
    __COLON, __AND, __OR, __EQUAL, __NEQUAL, \
    __SQUOTE, __DQUOTE, __CHAR, __STRING, __COMMENT = list(range(1, 44))


    # lookup table matching a lexeme to a specific token type. When the state machine
    # finds an identifier token, the tokenizer checks it against this table, and
    # if it matches one of the values, changes the return type to the corresponding
    # token type.
    resWords = {"BEGIN": BEGINTOK, "END": ENDTOK, \
                "INT": BASICTYPETOK, "CHAR": BASICTYPETOK, "INTCONST": INTCONSTTOK, \
                "STRING": BASICTYPETOK, "BOOLEAN": BASICTYPETOK, \
                "NOT": NOTTOK,
                "IF": IFTOK, "THEN": THENTOK, "ELSE": ELSETOK, "FI": FITOK, \
                "WHILE": WHILETOK, "DO": DOTOK, "OD": ODTOK, \
                "FOR": FORTOK, "ROF": ROFTOK, "UNTIL": UNTILTOK, "STEP": STEPTOK, \
                "PROC": PROCTOK, "ARRAY": ARRAYTOK, \
                "TRUE": BOOLLIT, "FALSE":BOOLLIT }


    # A simple lookup table for the names of the different token types. It is
    # probably possible to merge this with the lookup table above, but this
    # was the expedient solution given the long delays in completing the project.
    # Note that these need to align correctly with the enumerated constants, which
    # may cause maintanence problems later.
    token_desc = ['START', 'EOF', 'WSPACE', \
    'SEMI', 'BRACKET', 'PAREN', 'COMMA', \
    'IDENT', 'CHARLIT', 'INTLIT', 'STRINGLIT', 'BOOLLIT', \
    'MULOP', 'ADDOP', 'RELOP', 'NOTTOK', 'ASSIGN', \
    'BASICTYPETOK', 'INTCONSTTOK', 'ARRAYTOK', 'PROCTOK', \
    'BEGINTOK', 'ENDTOK', \
    'IFTOK', 'THENTOK', 'ELSETOK', 'FITOK', \
    'WHILETOK', 'DOTOK', 'ODTOK', \
    'FORTOK', 'ROFTOK', 'UNTILTOK', 'STEPTOK' ]

    # constant string representing the allowable characters in an identifier
    id_chars = ascii_letters + digits + '_'

    # class static initialization
    
    # Initialize the FSM to the start state, including all transitions out of it.
    fsm = StateMachine(
            State(
                {
                    '': EOF, whitespace: __WSPACE, '#': __COMMENT,
                    ascii_letters: IDENT, digits: INTLIT, "'": __SQUOTE, '"':__STRING,
                    '()': PAREN, '[]': BRACKET, ';': SEMI, ',': COMMA,
                    '+-': ADDOP, '*/%': MULOP, '<>': RELOP,
                    ':': __COLON, '&': __AND, '|': __OR,
                    '=': __EQUAL, '!': __NEQUAL,
                    State.OTHER: State.ERROR
                }))
    
    
    # add the list of states and their transitions to the FSM
    # end of file -> always accept
    fsm.add(EOF,
            State({State.OTHER: State.ACCEPT}, True, EOF, 0))
    # whitespace -> eat until the next valid input, then push back
    # one and return to start
    fsm.add(__WSPACE,
            State({whitespace: __WSPACE, State.OTHER: State.ACCEPT}, \
            True, __WSPACE, 1))
    # identifier -> eat until the last valid ID char, then accept and push back one
    fsm.add(IDENT,
            State({id_chars: IDENT, State.OTHER: State.ACCEPT}, True, IDENT, 1))
    # intlit -> eat all numbers, then accept
    fsm.add(INTLIT,
            State({id_chars: INTLIT, State.OTHER: State.ACCEPT},
            True, INTLIT, 1))
    # + or - -> accept and push back one
    fsm.add(ADDOP, State({State.OTHER: State.ACCEPT}, True, ADDOP, 1))
    # *, / or % -> accept and push back one
    fsm.add(MULOP, State({State.OTHER: State.ACCEPT}, True, MULOP, 1))
    # > or < -> accept and push back one
    fsm.add(RELOP, State({State.OTHER: State.ACCEPT}, True, RELOP, 1))
    # semicolon -> accept and push back one
    fsm.add(SEMI, State({State.OTHER: State.ACCEPT}, True, SEMI, 1))
    # comma -> accept and push back one
    fsm.add(COMMA, State({State.OTHER: State.ACCEPT}, True, COMMA, 1))
    # parenthesis -> accept and push back one
    fsm.add(PAREN, State({State.OTHER: State.ACCEPT}, True, PAREN, 1))
    # bracket -> accept and push back one
    fsm.add(BRACKET, State({State.OTHER: State.ACCEPT}, True, BRACKET, 1))
    # The following represent intermediate states in compound operators.
    # They are private to the class, unlike the others.
    # colon -> accept of the next char is an equals sign, otherwise fail
    fsm.add(__COLON, State({'=': State.ACCEPT}, True, ASSIGN, 0))
    # ampersand -> accept of the next char is an ampersand, otherwise fail
    fsm.add(__AND, State({'&': State.ACCEPT}, True, MULOP, 0))
    # vertical bar -> accept of the next char is a vertical bar, otherwise fail
    fsm.add(__OR, State({'|': State.ACCEPT}, True, ADDOP, 0))
    # equals sign -> accept of the next char is an equals sign, otherwise fail
    fsm.add(__EQUAL, State({'=': State.ACCEPT}, True, RELOP, 0))
    # exclamation point -> accept if the next char is an equals sign,
    # otherwise fail
    fsm.add(__NEQUAL, State({'=': State.ACCEPT}, True, RELOP, 0))
    # single quote -> continue for any following char except a single quote
    fsm.add(__SQUOTE, State({State.OTHER: __CHAR}))
    # character -> accept of the next char is an signle quote, otherwise fail
    fsm.add(__CHAR, State({"'": State.ACCEPT}, True, CHARLIT, 0))
    # double quote -> accept any number of characters until another double
    # quote is reached
    fsm.add(__STRING,
        State({'"': State.ACCEPT, State.OTHER: __STRING}, True, STRINGLIT, 0))
    # hash -> eat all inout to the end of the current line, then go back to start
    fsm.add(__COMMENT,
        State({'\n': State.ACCEPT, State.OTHER: __COMMENT}, True, __COMMENT, 0))

    # lock state machine after adding all the states
    fsm.lock()


    def __init__(self, toktype, line, lexeme):
        """ Constructor - create a new Token object.
        
        
       Each Token consists of a token type, the line # on which it
       was found, and the actual text of the lexeme.
       """
        self.__toktype, self.__line, self.__lexeme = toktype, line, lexeme

    @classmethod
    def Tokenizer(cls, buffer, wrng):
        """ Create generator for new tokens from the CharBuffer input.
       
        The class method takes a CharBuffer object and returns a
        generator function which iterates through the input source,
        returning each successive token.
        
        The generator itself begins each call by
       """
        # continue until the end of the file
        global warning
        warning = wrng
        while not buffer.eof():
            final = False       # clear the previous token state
            lexeme = ''
            
            # read the next character and, if it is not an end of file,
            # feed it to the FSM. If it is an EOF, return an EOF token and
            # break from the loop. Accumulate the read characters into the
            # string 'lexeme'.
            while not final:
                ch = buffer.getChar()
                if ch == '':
                    yield Token(cls.EOF, buffer.line(), '')
                    break
                final, toktype, pb = cls.fsm.transition(ch)
                lexeme += ch
            
            # If the FSM returns an error, print a warning and
            # go on to the mext token. Note that this has to check for the
            # end of line, as identifiers can be mistakenly reported as
            # errors if there is a newline in them.
            if toktype == State.ERROR and '\n' not in lexeme:
                warning(Token(State.ERROR, buffer.line(), lexeme),
                    "Invalid token " + lexeme + \
                    " on line " + str(buffer.line()))
                buffer.pushback(pb)
                lexeme = ''
                continue
                
            # if the FSM finds a comment or string of whitespace, push back
            # the first good character and continue to the next token
            if toktype == cls.__WSPACE or toktype == cls.__COMMENT:
                lexeme = ''
                buffer.pushback(pb)
                continue

            # if the token is a string literal, make sure it does not
            # have a newline in it
            if toktype == cls.STRINGLIT and '\n' in lexeme:
                warning(Token(State.ERROR, buffer.line(), lexeme),
                    " incomplete string on line " + str(buffer.line()))
                lexeme = ''
                buffer.pushback(pb)
                continue

            # push back any characters not eaten in the current string
            if (pb > 0):
                lexeme = lexeme[0:-pb]
                buffer.pushback(pb)

            # if the token is recognized as an identifier, check to see if
            # if is a keyword, and if it is, use the keyword token type
            # instead of IDENT
            if toktype == cls.IDENT:
                if lexeme.upper() in cls.resWords:
                    toktype = cls.resWords[lexeme.upper()]
            
            # return the completed token
            yield Token(toktype, buffer.line(), lexeme)
            
        # end of file reached - continue returning EOF tokens indefinitely
        while(True):
            yield Token(cls.EOF, buffer.line(), '')


    def __repr__(self):
        """String representation of a Token object.
       
        Just calls str()
       """
        return str(self)

    def __str__(self):
        """Simple string representation of a Token object.
       
       If the token is an ERROR token, return "ERROR".
       If it is a literal or an identifier, return type name and the lexeme,
       Otherwise, return just the name of the type.
       """
        if self.__toktype == State.ERROR:
            return "ERROR"
        elif self.__toktype in [self.CHARLIT, self.INTLIT, self.BOOLLIT, \
                                self.STRINGLIT, self.IDENT, self.BASICTYPETOK]:
            return (self.token_desc[self.__toktype] + '(' + self.__lexeme + ')')
        else:
            return self.token_desc[self.__toktype]

    def line(self):
        """Return the line on which  the token was found."""
        return self.__line

    def type(self):
        """Return a string with the name of the token type."""
        return self.__toktype
    
    def value(self):
        """Return the token's lexeme."""
        return self.__lexeme



######################################
## test code
if __name__ == "__main__":
    
    def wr(tok, msg):
        print("bad " + str(tok) + ' ' + msg)
        
    get = Token.Tokenizer(CharBuffer(open("assign-test.al")), wr)
    tok = next(get)

        
    while tok.type() != Token.EOF:
        print(tok, ':', repr(tok))
        tok = next(get)
