
# part of the Suntiger Algol project
# initiated 2008:05:23, by Alice Osako <alicetrillianosako@gmail.com>
# file last modified 2022:02:11


import sys, os
from tokens import Token
from labels import *
from Symbol import *
from SymbolTable import *
from MasterSymbolTable import *


# global constants for the symbol table and stack offsets.
# While I feel I should find some better way to organize these,
# I've done this for now as a matter of expedience.

symtab = None

def parse(src, out, print_listing, st, warning, error, emit, load, store):
    """ parse() - the main parsing function.
    
    This function serves as an outer scope for the functions
    inside of it, specifically for the file source, output file
    and listing file variables.
    
    The actual code for the function is below all of the sub-functions.
    """
    global symtab
    symtab = st
    
    def match(tok, toktype, lexeme = None):
        """ Match a token against a token type and an optional
        lexeme.
        
        Match first checks the type of the token against toktype.
        If they match, it then checks it against the lexeme argument,
        if any. If it matches the arguments, it prints the listing
        and returns the next token. If it does not match, it gives
        a fatal error (and returns None, though it won't get there).
       """
        if tok.type() == toktype:
            if (lexeme is None) or (lexeme==tok.value()):
                print_listing(tok)
                return next(src)
        error(tok, " found, " + Token.token_desc[toktype] + " expected")
        return None
    
    def match_in(tok, toktypes):
        """ Match a token with one of a list or dict of token types.
       
        Tests to see if the token type matches one of the types
        listed in toktype. If it matches, it prints the listing
        and returns the next token. If it does not match, it gives
        a fatal error (and returns None, though it won't get there).
       """
        if tok.type() in toktypes:
            print_listing(tok)
            return next(src)
        error(tok,  ", other statement or expression expected")
        return None
    
    def program(tok):
        """ Parse program """
        endtok = blockst(tok)   # program -> blockst
        eoftok = match(endtok, Token.EOF)
    
    def blockst(tok):
        # blockst -> BEGINTOK stats ENDTOK
        nexttok = match(tok, Token.BEGINTOK)
        # set up local symbol table
        syms, blocknum = symtab.size()
        blocknum += 1
        symtab.enter("block" + str(blocknum))
        endtok = stats(nexttok)
        eoftok = match(endtok, Token.ENDTOK)
        symtab.exit("block" + str(blocknum))
        return eoftok

    def stats(tok):
        firsts = [Token.BEGINTOK, Token.IDENT, \
                Token.BASICTYPETOK, Token.INTCONSTTOK, \
                Token.IFTOK, Token.WHILETOK]
        finals = [Token.ENDTOK, Token.FITOK, Token.ODTOK]
        
        if tok.type() in firsts:
            # stats -> statmnt SEMI stats
            semitok = statmnt(tok)
            if semitok not in finals:
                endtok = match(semitok, Token.SEMI)
                return stats(endtok)
            else:
                return semitok
        else:   # stats -> NULL
            return tok
         
            
    def statmnt(tok):
        """ Parse an individual statement."""
        
        # lookup table matching token types with parsing functions
        firsts = {Token.BEGINTOK: blockst, Token.IDENT: idstat, \
                Token.BASICTYPETOK: decl, \
                Token.INTCONSTTOK: decl, \
                Token.IFTOK: ifstat, Token.WHILETOK: loopstat}
                
        # statmnt -> blockst | idstat | decl | ifstat | loopstat
        # This looks up type of tok in the
        if tok.type() in firsts:
            cont = firsts[tok.type()]
            closetok = cont(tok)
            free_temps()
            return closetok
        else:           # statmnt ->
            error(tok, "statement expected.")
    
    def decl(tok):
        if tok.type() == Token.INTCONSTTOK:     # decl -> constdecl
            closetok = constdecl(tok)
            return closetok
        elif tok.type() == Token.BASICTYPETOK:
            closetok = vardecl(tok)         # decl -> vardecl
            return closetok
        else:
            error(tok, "Declaration expected.")
        
    def constdecl(tok):
        global symtab, currOffset
        
        # constdecl -> identifier ASSIGN INTLIT
        decltok = match(tok, Token.INTCONSTTOK)
        assgntok, type, location = identifier(decltok)
        valtok = match(assgntok, Token.ASSIGN)
        closetok = match(valtok, Token.INTLIT)
        if symtab.find(decltok.value().upper()):
            error(decltok, " redeclaration error.")
        syms, blocks = symtab.size()
        offset = -(syms * 4)
        symtab.insert(Constant(decltok.value().upper(), \
                        valtok.value().upper(), offset - 4))
        
        return closetok
                    
    def vardecl(tok):
        global symtab
        
        # vardecl -> BASICTYPETOK IDENTIFIER
        decltok = match(tok, Token.BASICTYPETOK)
        closetok, type, location = identifier(decltok)
        if symtab.find(decltok.value().upper()):
            error(decltok, " redeclaration error.")
        syms, blocks = symtab.size()
        offset = -(syms * 4)
        symtab.insert(Variable(decltok.value().upper(), \
                        tok.value().upper(), offset - 4))
        return closetok
    
    def idstat(tok):
        global symtab
        # idstat -> IDENT moreid
        nexttok, itype, ilocation = identifier(tok)
        sym = symtab.find_in_scope(tok.value().upper())
        if not sym:
            print(symtab)
            error(tok, ": identifier not found.")
        closetok = moreid(nexttok, sym, tok)
        return closetok
        
    def moreid(tok, sym, target):
        global symtab
        
        # moreid -> ASSIGN expression
        if tok.type() == Token.ASSIGN:
            exprtok = match(tok, Token.ASSIGN)
            closetok, etype, elocation = expression(exprtok)
            if not isinstance(sym, Variable):
                error(target, " not a valid l-value.")
            elif etype == "STRING":
                emit('la $t0, ' + elocation)
                emit('sw $t0, ' + str(sym.location()) + '($sp)')
            else:
                load('$t1', elocation, etype)
                store('$t1', sym.location(), etype)
            return closetok
        else:
            # moreid -> PAREN expression PAREN
            exprtok = match(tok, Token.PAREN, '(')
            
            if isinstance(sym, SystemRoutine):
                if sym.getName() == "PRINTLN":
                    code = sym.code(None)
                    out.write(code)
                    rpartok = exprtok
                else:
                    rpartok, etype, elocation = expression(exprtok)
                    code = sym.code(etype)
                    if not code:
                        error(exprtok, " does not take " + etype + " arguments")
                    else:
                        if etype in ["INT", "BOOLEAN"]:
                            load('$a0', elocation, etype)
                        elif etype == 'CHAR':
                            load('$t1', elocation, etype)
                            emit('sb $t1, charSwap')
                            emit('la $a0, charSwap')
                        elif etype == "STRING":
                            if isinstance(elocation, int):
                                emit('lw $a0, ' + str(elocation) + '($sp)')
                            elif elocation[0] == '$':
                                emit('move $a0, ' + elocation)
                            else:
                                emit('la $a0, ' + elocation)
                        
                        out.write(code)
                closetok = match(rpartok, Token.PAREN, ')')
                return closetok
            
        error(exprtok, " not found.")

            
    def ifstat(tok):
        # ifstat -> IFTOK expression THEN stats moreif
        exprtok = match(tok, Token.IFTOK)
        thentok, etype, elocation = expression(exprtok)
        if etype != "BOOLEAN":
            error(tok, " not a boolean expression.")
        load('$t1', elocation, etype)
        elseLabel = get_label('else')
        emit('beq $zero, $t1, ' + elseLabel)
        statstok = match(thentok, Token.THENTOK)
        moretok = stats(statstok)
        return moreif(moretok, elseLabel)
        
    def moreif(tok, label):
        if tok.type() == Token.FITOK:       # moreif -> FITOK
            out.write(label + ':\n')
            return match(tok, Token.FITOK)
        else:                               #moreif -> ELSETOK stats FITOK
            elstok = match(tok, Token.ELSETOK)
            fiLabel = get_label('fi')
            emit('j ' + fiLabel)
            out.write(label + ':\n')
            fitok = stats(elstok)
            out.write(fiLabel + ':\n')
            return match(fitok, Token.FITOK)
        
    def loopstat(tok):
        # loopstat -> WHILETOK expression DOTOK stats ODTOK
        exprtok = match(tok, Token.WHILETOK)
        doLabel = get_label("while")
        endLabel = get_label('od')
        out.write(doLabel + ':\n')
        dotok, etype, elocation = expression(exprtok)
        if etype != "BOOLEAN":
            error(tok, " not a conditional expression.")
        statstok = match(dotok, Token.DOTOK)
        load('$t1', elocation, etype)
        emit('beq $zero, $t1, ' + endLabel)
        odtok = stats(statstok)
        emit('j ' + doLabel)
        out.write(endLabel + ':\n')
        return match(odtok, Token.ODTOK)
        
    def expression(tok):
        # expression -> term expprime
        expptok, ttype, tlocation = term(tok)
        closetok, eptype, eplocation = expprime(expptok, ttype, tlocation)
        if eptype is None:
            return expptok, ttype, tlocation
        else:
            return closetok, eptype, eplocation
            
    def expprime(tok, ltype, location):
        # expprime -> ADDOP term expprime
        if tok.type() == Token.ADDOP:
            termtok = match(tok, Token.ADDOP)
            expptok, rtype, rlocation = term(termtok)
            if ltype != rtype:
                error(tok, ' not a valid mathematical expression.')
            load('$t1', location, ltype)
            load('$t2', rlocation, rtype)
            temp = get_temp()
            if ltype == 'INT':
                if tok.value() == '+':
                    emit('add $t1, $t1, $t2')
                    store('$t1', temp, 'INT')
                elif tok.value() == '-':
                    emit('sub $t1, $t1, $t2')
                    store('$t1', temp, 'INT')
                else:
                    error(tok, " not an arithmetic operator")
            elif ltype == 'BOOLEAN':
                if tok.value() == '||':
                    emit('or $t1, $t1, $t2')
                    store('$t1', temp, 'BOOLEAN')
                else:
                    error(tok, " not a boolean operator")
            return expprime(expptok, ltype, temp)
        else:       # expprime -> NULL
            return tok, ltype, location
        
    def term(tok):
        # term -> relfactor termprime
        termptok, rtype, rlocation = relfactor(tok)
        closetok, ttype, tlocation = termprime(termptok, rtype, rlocation)
        if ttype is None:
            return termptok, rtype, rlocation
        else:
            return closetok, ttype, tlocation

            
    def termprime(tok, ltype, location):
        # termprime -> MULOP relfactor termprime
        if tok.type() == Token.MULOP:
            reltok = match(tok, Token.MULOP)
            termptok, rtype, rlocation = relfactor(reltok)
            if ltype != rtype:
                error(tok, ' not a valid mathematical term.')
            load('$t1', location, ltype)
            load('$t2', rlocation, rtype)
            temp = get_temp()
            if ltype == 'INT':
                if tok.value() == '*':
                    emit('mult $t1, $t2')
                    emit('mfhi $t1')
                    emit('mflo $t2')
                    store('$t2', temp, 'INT')
                elif tok.value() == '/':
                    emit('div $t1, $t2')
                    emit('mflo $t1')
                    store('$t1', temp, 'INT')
                elif tok.value() == '%':
                    emit('div $t1, $t2')
                    emit('mfhi $t1')
                    store('$t1', temp, 'INT')
                else:
                    error(tok, " not an arithmetic operator")
            elif ltype == 'BOOLEAN':
                if tok.value() == '&&':
                    emit('and $t1, $t1, $t2')
                    store('$t1', temp, 'BOOLEAN')
                else:
                    error(tok, " not a boolean operator")
            return termprime(termptok, ltype, temp)
        else:           # termprime -> NULL
            return tok, ltype, location
        
    def relfactor(tok):
        # relfactor -> factor factorprime
    
        reltok, ftype, flocation = factor(tok)
        closetok, rtype, rlocation = factorprime(reltok, ftype, flocation)
        if rtype is None:
            return reltok, ftype, flocation
        else:
            return closetok, rtype, rlocation

    def factorprime(tok, ltype, location):
        relops = {'==':'beq $zero,', '!=':'bne $zero,', '<':'blez', '>':'bgtz'}
        # factorprime -> RELOP factor
        if tok.type() == Token.RELOP:
            facttok = match(tok, Token.RELOP)
            closetok, ftype, flocation = factor(facttok)
            if ftype != ltype:
                error(facttok, " type mismatch in comparison")
            load('$t1', location, ltype)
            load('$t2', flocation, ftype)
            emit('sub $t1, $t1, $t2')
            true_label = get_label('true')
            false_label = get_label('false')
            temp = get_temp()
            emit(relops.get(tok.value()) + ' $t1, ' + true_label)
            store('$zero', temp, 'BOOLEAN')
            emit('j ' + false_label)
            out.write(true_label + ':\n')
            emit('li $t1, 1')
            store('$t1', temp, 'BOOLEAN')
            out.write(false_label + ':\n')
            return closetok, 'BOOLEAN', temp
        else:       # factorprime -> NULL
            return tok, ltype, location
        
    def factor(tok):
        # list of literal types for matching
        literals = {Token.INTLIT: "INT",
                    Token.CHARLIT: "CHAR",
                    Token.BOOLLIT: "BOOLEAN",
                    Token.STRINGLIT: "STRING"}
        
        if tok.type() == Token.NOTTOK: # factor -> NOTTOK factor
            nottok = match(tok, Token.NOTTOK)
            return factor(nottok)
        elif tok.type() == Token.IDENT: # factor -> identifier
            closetok, type, location = identifier(tok)
            if type is None or location is None:
                error(tok, " not declared in this scope.")
            return closetok, type, location
        elif tok.type() in literals:    # factor -> LITERAL
            closetok = match_in(tok, literals)  # can match with any lit types
            label = addlit(tok)
            return closetok, literals[tok.type()], label
        elif tok.type() == Token.PAREN:
            # factor -> PAREN expression PAREN
            exprtok = match(tok, Token.PAREN, '(')
            rpartok, etype, elocation = expression(exprtok)
            closetok = match(rpartok, Token.PAREN, ')')
            return closetok, etype, elocation
        else:
            error(tok, ", factor expected.")
                
    def identifier(tok):
        # identifier -> IDENT
        closetok = match(tok, Token.IDENT)
        sym_entry = symtab.find_in_scope(tok.value().upper())
        if not sym_entry or not isinstance(sym_entry, Variable):
            return closetok, None, None
        else:
            return closetok, sym_entry.type(), sym_entry.location()
    
    
    # main parse function initializer
    symtab.insert(SystemRoutine("PRINTLN",
                                "\tla $a0, nl\n\tli $v0, 4\n\tsyscall\n",
                                [None]))
    symtab.insert(SystemRoutine("PRINTI",
                                "\tli $v0, 1\n\tsyscall\n",
                                ["INT"]))
    symtab.insert(SystemRoutine("PRINTC",
                                "\tli $v0, 4\n\tsyscall\n",
                                ["CHAR"]))
    symtab.insert(SystemRoutine("PRINTS",
                                "\tli $v0, 4\n\tsyscall\n",
                                ["STRING"]))
    symtab.insert(SystemRoutine("PRINTB",
                                '\tla $t0, boolLookup\n' \
                                + '\tsll $a0, $a0, 2\n'
                                + '\tadd $t0, $a0, $t0\n' \
                                + '\tlw $a0, 0($t0)\n' \
                                + '\tli $v0, 4\n\tsyscall\n',
                                ["BOOLEAN"]))

    # S -> program
    program(next(src))


